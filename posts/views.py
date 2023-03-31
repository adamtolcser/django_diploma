from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import authentication
from rest_framework import status, serializers
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from posts.models import Post


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class GetPostSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'date_created', 'date_updated', 'user']


class GetPostByIdSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'date_created', 'date_updated', 'user']


class PutPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class Posts(ListCreateAPIView):
    model = Post
    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(
        request=GetPostSerializer,
        responses=GetPostSerializer,
    )
    def list(self, args, **kwargs):
        all_posts = Post.objects.all()
        serializer = GetPostSerializer(all_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=AddPostSerializer,
        responses=AddPostSerializer,
    )
    def post(self, args, **kwargs):
        try:
            title = self.request.data.get('title', '')
            body = self.request.data.get('body', '')
            user_id = self.request.user.id
            serializer = AddPostSerializer(data={'title': title, 'body': body})
            serializer.is_valid(raise_exception=True)
            return self.insert_post([title, body, user_id])
        except Exception:
            return Response(data={'message': 'Failed to create object!'}, status=status.HTTP_400_BAD_REQUEST)

    def insert_post(self, data):
        Post.objects.create(title=data[0], body=data[1], user_id=data[2])
        return Response(data={'message': 'Object created!', 'title': data[0], 'body': data[1]},
                        status=status.HTTP_201_CREATED)


class PostById(ListAPIView):
    model = Post
    authentication_classes = [authentication.TokenAuthentication]

    def list(self, request, **kwargs):
        post_id = kwargs['id']
        post = get_object_or_404(Post, id=post_id)
        serializer = GetPostByIdSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PutPostSerializer,
        responses=PutPostSerializer,
    )
    def put(self, request, **kwargs):
        try:
            post_id = kwargs['id']
            post = get_object_or_404(Post, id=post_id)
            serializer = PutPostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValueError
        except ValueError:
            return Response(data={'message': 'Failed to update object!'}, status=status.HTTP_400_BAD_REQUEST)