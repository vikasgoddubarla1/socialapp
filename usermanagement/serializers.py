from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    confirmpassword = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'username', 'password', 'confirmpassword', 'email', 'profile_photo', 'bio', 'is_private_account', 'is_admin', 'city', 'state', 'country_id')
               

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'username', 'email', 'profile_photo', 'bio', 'is_private_account', 'is_admin', 'city', 'state', 'country_id')
            
        
class UserLoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_id', 'browser', 'operating_system', 'device', 'ip_address', 'last_login')
        
#------------------------------------------------------- FOLLOW USER SERIALIZER ----------------------------------------------------------

class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = ('id', 'following', 'follower', 'request_status', 'created_at')
        
class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = ('id', 'block_user_id', 'blocked_by_user', 'created_at')
        

        
class UserDetailSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'username', 'email', 'profile_photo', 'bio', 'is_private_account', 'is_admin', 'city', 'state', 'country_id', 'following', 'followers')
    
    def get_following(self, obj):
        followings = FollowUser.objects.filter(following=obj, request_status = 'approved').count()
        return followings if followings is not None else 0
        # return [
        #     {
        #         'id':following.following.id,
        #         'username':following.following.username,
        #         'request_status':following.request_status,
        #         'created_at':following.created_at
                
        #     }
        #     for following in followings
        # ]
    
    def get_followers(self, obj):
        followers = FollowUser.objects.filter(follower=obj, request_status='approved').count()
        return followers if followers is not None else 0
        # return [
        #     {
                
        #         'id':follower.id,
        #         'username':follower.follower.username,
        #         'request_status':follower.request_status,
        #         'created_at':follower.created_at
        #     }
        #     for follower in followers
        # ]
        
        
class UserFollowersListSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'followers')

    
    def get_followers(self, obj):
        followers = FollowUser.objects.filter(follower=obj, request_status='approved')
        return [
            {
                
                'id':follower.id,
                'username':follower.follower.username,
                'request_status':follower.request_status,
                'created_at':follower.created_at
            }
            for follower in followers
        ]
        
class UserFollowingsListSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'followings')

    
    def get_following(self, obj):
        followings = FollowUser.objects.filter(following=obj, request_status = 'approved')
        return [
            {
                'id':following.following.id,
                'username':following.following.username,
                'request_status':following.request_status,
                'created_at':following.created_at
                
            }
            for following in followings
        ]