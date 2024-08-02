from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Country)
admin.site.register(User)
admin.site.register(RecoveryCode)
admin.site.register(UserLoginLogs)
admin.site.register(FollowUser)
admin.site.register(BlockUser)
