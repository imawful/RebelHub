from django.shortcuts import render
from rest_framework import generics, status, filters
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer, LikePostSerializer, DislikePostSerializer, PostEditSerializer, PostTagSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from .helper import filter_queryset

# Create your views here

# Able to create and view the post, should only handles POST requests to create a post
class CreatePost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    
        
# Delete the post by its ID
class PostDelete(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    def perform_destroy(self, instance):
        user = self.request.user
        if user != instance.author:
            if user != instance.hub.owner:
                if user not in instance.hub.mods.all():
                    raise PermissionDenied("Could Not Delete Post: You are not post author, hub owner, or a hub moderator")
        instance.delete()



# Able to view a list of all post, should only handles GET requests to Fetch a list of all post 
class PostList(generics.ListAPIView): 
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(hub__in=user.joined_hubs.all())

    

# Get the post by its ID or return a 404 error if not found
class LikePost(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikePostSerializer
    lookup_field = "id"

# Get the post by its ID or return a 404 error if not found
class DislikePost(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DislikePostSerializer
    lookup_field = "id"

# GET a single post by its ID
class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            qs = Post.objects.all()
        else:
            qs = Post.objects.filter(hub__private_hub=False)
        if qs is None:
            raise NotFound("No Post with this ID was found")
        return qs

# GET a list of posts for the explore page.
# Explore page includes all posts from public hubs and posts from private hubs that the user has joined
# Can be filtered by timestamp (past 24 hours, week, month, year, or all time) 
# and ordered by likes (ascending or descending) or timestamp (new or old)
class ExploreList(generics.ListAPIView): 
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        
        queryset = Post.objects.filter(Q(hub__private_hub=False) | Q(hub__in=user.joined_hubs.all())).prefetch_related('comments')
        return filter_queryset(self, queryset) # Uses filter_queryset function from helper.py to filter and sort posts
      
# Edit a single post by its ID
class PostEdit(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostEditSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def perform_update(self, serializer):
        serializer.save()

# Add or remove a hub tag from a post
class PostTag(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostTagSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def perform_update(self, serializer):
        serializer.save()

