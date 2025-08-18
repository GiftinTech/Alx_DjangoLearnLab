from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

class IsAuthorOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.author == request.user

class StandardResultsSetPagination(PageNumberPagination):
  page_size = 10
  page_size_query_param = 'page_size'
  max_page_size = 50

class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all().order_by('-created_at')
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
  pagination_class = StandardResultsSetPagination
  filter_backends = [filters.SearchFilter]
  search_fields = ['title', 'content']

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all().order_by('-created_at')
  serializer_class = CommentSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
  pagination_class = StandardResultsSetPagination

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    # Get users the current user follows
    following_users = self.request.user.following.all()
    # Get posts from them
    return Post.objects.filter(author__in=following_users).order_by("-created_at")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
  try:
    post = Post.objects.get(pk=pk)
  except Post.DoesNotExist:
    return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

  like, created = Like.objects.get_or_create(post=post, user=request.user)
  if not created:
    return Response({"message": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

  # Create notification
  if post.author != request.user:  # don’t notify self
    Notification.objects.create(
      recipient=post.author,
      actor=request.user,
      verb="liked your post",
      target=post,
    )

  return Response({"message": "Post liked!"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
  try:
    post = Post.objects.get(pk=pk)
  except Post.DoesNotExist:
    return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

  try:
    like = Like.objects.get(post=post, user=request.user)
    like.delete()
    return Response({"message": "Post unliked!"}, status=status.HTTP_200_OK)
  except Like.DoesNotExist:
    return Response({"message": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)
