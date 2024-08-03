from django.db import models
from usermanagement.models import User

def user_post_upload_to(instance, filename):
    return f'media/user_{instance.posted_by.id}/posts/{filename}'

# Create your models here.
class Posts(models.Model):
    post_type = models.CharField(max_length=55, choices=[
        ('image', 'image'),
        ('video', 'video'),
    ])
    post_image = models.FileField(upload_to=user_post_upload_to)
    description = models.TextField(null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comments_allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'posts'
    

class PostTags(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = 'post tags'
    
class PostLikes(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = 'post likes'
    
class PostComments(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    parent_comment_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_at = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = 'comments'
    
class PostCommentLikes(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    post_comment_id = models.ForeignKey(PostComments, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = 'post comment likes'
    