from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Posts)
admin.site.register(PostTags)
admin.site.register(PostLikes)
admin.site.register(PostComments)
admin.site.register(PostCommentLikes)