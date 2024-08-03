
from django.urls import path
from .views import *

urlpatterns = [
    #---------------------------- POSTS ------------------------------------------------------
    path('post/create', CreatePost.as_view(), name='post-create'),
    path('post/update/<int:pk>', UpdatePost.as_view(), name='update-post'),
    path('post/delete/<int:pk>', PostDelete.as_view(), name='delete-post'),
    path('post/detail/<int:user_id>', PostByUser.as_view(), name='user-posts'),
    
    #---------------------------------- POST TAGS ----------------------------------------------
    path('post/tags/create', CreatePostTags.as_view(), name='post-tags-create'),
    
    #---------------------------------- POST LIKES --------------------------------------
    path('post/like/create', CreatePostLikes.as_view(), name='post-like-create'),
    path('post/like/delete/<int:pk>', DeletePostLikes.as_view(), name='post-like-delete'),
    
    #--------------------------------------- POST COMMENTS ------------------------------------
    path('post/comment/create', CreatePostComments.as_view(), name='post-comment-create'),
    path('post/comment/update/<int:pk>', UpdatePostComment.as_view(), name='post-comment-update'),
    path('post/comment/delete/<int:pk>', DeletePostComment.as_view(), name='post-comment-delete'),
    
    #---------------------------------- POST COMMENT LIKES --------------------------------------
    path('post/comment/like/create', CreatePostCommentLikes.as_view(), name='post-comment-like-create'),
    path('post/comment/like/delete/<int:pk>', DeletePostCommentLikes.as_view(), name='post-comment-like-delete'),
    
    
    
    
    
    
]
