from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Показываем только посты, созданные текущим пользователем для редактирования."""
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            return Response({'detail': 'У вас нет прав для редактирования этого поста.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Показываем только комментарии, созданные текущим пользователем для редактирования."""
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            return Response({'detail': 'У вас нет прав для редактирования этого комментария.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if created:
            return Response({'detail': 'Лайк добавлен.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Вы уже лайкнули этот пост.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        like = get_object_or_404(Like, post=post, user=request.user)
        like.delete()
        return Response({'detail': 'Лайк удален.'}, status=status.HTTP_204_NO_CONTENT)
