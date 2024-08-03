from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response    
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# Create your views here.

class CreatePost(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'post created successfully!'})
    
class UpdatePost(generics.UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message':'post updated successfully!'})
        except Exception as e:
            return Response({'error':str(e)}, status=400)

#This will return all the likes, comments, comment likes, replies to comments handling from serializer
class PostByUser(generics.RetrieveAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get('user_id')
            user = Posts.objects.filter(posted_by=user_id)
            instance = self.get_queryset()
            serializer = self.get_serializer(instance, many=True)
            return Response({'postDetail':serializer.data})
        except Exception as e:
            return Response({'error':str(e)}, status=400)
    
class PostDelete(generics.DestroyAPIView):
    queryset = Posts.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user_id:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'message':'post deleted successfully!'})

#------------------------------------- POST TAGS -------------------------------------------------
#this api work for update, delete and create!
class CreatePostTags(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        try:
            post_id = request.data.get('post_id')
            user_id = request.data.get('user_id', [])
            users = User.objects.filter(pk__in=user_id)
            PostTags.objects.filter(post_id=post_id).delete()
            post = Posts.objects.get(pk=post_id)
            for user in users:
                PostTags.objects.create(
                    post_id = post,
                    user_id = user,
                    created_at= timezone.now()
                )
            return Response({'message':'users added to posts'})
        except Exception as e:
            return Response({'error':str(e)}, status=400)

#------------------------------- POST LIKES -----------------------------------------------------

class CreatePostLikes(generics.CreateAPIView):
     serializer_class = PostLikesSerializer
     permission_classes = (IsAuthenticated,)
     
     def create(self, request, *args, **kwargs):
         serializer = self.get_serializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response({'message':'post liked successfully!'})
     
class DeletePostLikes(generics.DestroyAPIView):
    serializer_class = PostLikesSerializer
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user_id:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'message':'post disliked successfully!'})
    
#---------------------------------- POST COMMENTS AND COMMENT LIKES --------------------------------

class CreatePostComments(generics.CreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'comment added successfully!'})
    
class UpdatePostComment(generics.UpdateAPIView):
    queryset = PostComments.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            if instance.user_id != request.user:
                return Response({'error':'You do not have permission to perform this action'}, status=400)
            serializer.save()
            return Response({'message':'comment updated successfully'})
        except Exception as e:
            return Response({'error':str(e)}, status=400)
    
class DeletePostComment(generics.DestroyAPIView):
    queryset = PostComments.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id != request.user:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'message':'comment deleted successfully!'})
    
#---------------------------------- POST COMMENT LIKES ----------------------------------------------
class CreatePostCommentLikes(generics.CreateAPIView):
     serializer_class = PostCommentLikesSerializer
     permission_classes = (IsAuthenticated,)
     
     def create(self, request, *args, **kwargs):
         serializer = self.get_serializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response({'message':'post liked successfully!'})
     
class DeletePostCommentLikes(generics.DestroyAPIView):
    serializer_class = PostCommentLikesSerializer
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user_id:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'message':'post disliked successfully!'})
 
    
        

    
