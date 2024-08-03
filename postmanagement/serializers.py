from rest_framework import serializers
from .models import *



class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTags
        fields = '__all__'
        
class PostLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = '__all__'
        

        
class PostCommentLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentLikes
        fields = '__all__'
        

class PostCommentSerializer(serializers.ModelSerializer):
    post_comment_likes = PostCommentLikesSerializer(source='postcommentlikes_set', many=True, read_only=True)
    class Meta:
        model = PostComments
        fields = '__all__'
        

class PostSerializer(serializers.ModelSerializer):
    post_tags = PostTagsSerializer(source='posttags_set', many=True, read_only=True)
    post_likes = PostLikesSerializer(source='postlikes_set', many = True, read_only=True)
    post_comments = PostCommentSerializer(source='postcomments_set', many=True, read_only=True)
    class Meta:
        model = Posts
        fields = ('id', 'post_type', 'post_image', 'posted_by', 'comments_allowed', 'created_at', 'post_tags', 'post_likes', 'post_comments')