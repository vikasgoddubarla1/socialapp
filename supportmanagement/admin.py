from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SupportContact)
admin.site.register(ReportOption)
admin.site.register(ReportUser)
admin.site.register(CommentReport)
admin.site.register(PostReport)