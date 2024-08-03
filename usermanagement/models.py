from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password


def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB
    if value.size > max_size:
        raise ValidationError({"status_code":604, "error":"profile photo must be less than 5MB"})
    
def profile_photo(instance, filename):
    filename = f"profile_photo_{instance.id}{filename[-4:]}"
    return f"users/profile_photo/{filename}"

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=255)
    phone_code = models.CharField(max_length=10)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    zone_name = models.CharField(max_length=100)
    gmtoffsetname = models.CharField(max_length=100, null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = 'contries'
    
    def __str__(self):
        return self.name
    
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValidationError({'error':'User must have an email'})
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create(email, username, password, **extra_fields)
        
class User(AbstractBaseUser):
    firstname = models.CharField(max_length=55)
    lastname = models.CharField(max_length=55)
    username = models.CharField(max_length=55, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    profile_photo = models.ImageField(upload_to='media/users/profile_photo', blank=True, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), validate_file_size,
    ], )
    bio = models.TextField(max_length=2000, null=True, blank=True)
    is_private_account = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country_id = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    objects = MyUserManager()
    
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    
    
class RecoveryCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    codes = models.TextField() #Recommended JsonField
    
    def __str__(self):
        return str(self.user)  
    



class UserForgotPassword(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code    = models.CharField(max_length=200, null=True, blank=True)
    expired_at = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user_id)
    

    
class UserLoginLogs(models.Model):
    user_id             = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    browser             = models.CharField(max_length=300, null=True, blank=True)
    operating_system    = models.CharField(max_length=300, null=True, blank=True)
    device             = models.CharField(max_length=300, null=True, blank=True)
    ip_address          = models.CharField(max_length=300, null=True, blank=True)
    last_login          = models.DateTimeField(max_length=300, null=True, blank=True)
    
    def __str__(self):
        return str(self.user_id)
    
    class Meta:
        verbose_name_plural = "User login logs"
        
        
#-------------------------------------------------------------- USER FOLLOW REQUESTS ------------------------------------------------------------

class FollowUser(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow')
    follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follower')
    request_status = models.CharField(max_length=100, choices=[
        ('approved', 'approved'), 
        ('pending', 'pending'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
class BlockUser(models.Model):
    block_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user')
    blocked_by_user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by_user')
    created_at = models.DateTimeField(auto_now_add=True)