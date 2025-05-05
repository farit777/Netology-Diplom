from rest_framework import serializers
from .models import Post, Comment, Like, Image

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at', 'comments', 'likes_count', 'images', 'location', 'latitude', 'longitude']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            image = Image.objects.create(**image_data)
            post.images.add(image)
        return post

    def get_likes_count(self, obj):
        return obj.likes.count()
