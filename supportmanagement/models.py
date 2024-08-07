from django.db import models
from usermanagement.models import User
from postmanagement.models import Posts, PostComments
# Create your models here.
class SupportContact(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=55, default='todo', choices=[
        ('todo', 'todo'),
        ('inprogress', 'inprogress'),
        ('hold', 'hold'),
        ('closed', 'closed')
    ])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    

class ReportOption(models.Model):
    name = models.CharField(max_length=1055, unique=True)
    created_at = models.DateTimeField()

class PostReport(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportOption, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField()
    
class CommentReport(models.Model):
    comment_id = models.ForeignKey(PostComments, on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportOption, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField()
    
class ReportUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    report_type = models.ForeignKey(ReportOption, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_by_user')
    created_at = models.DateTimeField()
    