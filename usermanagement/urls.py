
from django.urls import path
from .views import *

urlpatterns = [
    path('user/list', ListUser.as_view(), name='user-list'),
    path('user/create', CreateUser.as_view(), name='user-create'),
    path('user/get/<int:pk>', UserRetrieve.as_view(), name='user-retrieve-by-user'),
    path('user/update/<int:pk>', UpdateUser.as_view(), name='user-update'),
    path('user/delete/<int:pk>', DeleteUser.as_view(), name='user-delete'),
    path('user/create', ChangePassword.as_view(), name='user-change-password'),
    
    #------------------------------ USER FOLLOWER AND FOLLOWING LIST -------------------------------------------
    
    path('user/get/followers/<int:pk>', UserFollowersRetrieve.as_view(), name='user-retrieve-followers'),
    path('user/get/following/<int:pk>', UserFollowingRetrieve.as_view(), name='user-retrieve-followings'),
    
    
    #---------------------------- CLIENT TOKENS -----------------------------------
    path('client/token', TokenViewClient.as_view(), name='client-tokens-get'),
    path('client/refresh', ClientRefreshToken.as_view(), name='refresh-token-get'),
    path('client/login', UserLogin.as_view(), name='user-login'),
    path('client/logout', Logout.as_view(), name='user-logout'),
    
    #--------------------------------- TWO FACTOR AUTHENTICATION ----------------------------------
    
    path('user/generate/recoveryCodes', GenerateRecoveryCodes.as_view(), name='user-recoverycode-create'),
    path('user/2fa/enable', Enable2FA.as_view(), name='user-enable-2fa'),
    path('user/2fa/verify', Verify2FA.as_view(), name='user-verify-2fa'),
    path('user/verified/login', LoginAfterVerify.as_view(), name='login-after-verify'),
    path('user/2fa/disable', Disable2FA.as_view(), name='user-disable-2fa'),
    
    #---------------------------------- USER LOGS----------------------------------------------------
    path('user/logs/<int:user_id>', UserLoginLogsByUser.as_view(), name='user-logs-by-user'),
    
]
