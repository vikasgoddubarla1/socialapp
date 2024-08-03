from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dotenv import load_dotenv
import random, string, os, requests, json, qrcode, base64
from django.contrib.auth import authenticate
from io import BytesIO
from oauth2_provider.models import AccessToken, RefreshToken, Application
from socialapp.settings import URL_SCHEME
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .functions import *
# Create your views here.



#----------------------------------------------------------USER VIEWS ------------------------------------------------------------------------
class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'userDetails':serializer.data})
    
class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    # permission_classes = (IsAuthenticated,)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'userList':serializer.data})
    
class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    # permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'userDetails':serializer.data})
    
class UpdateUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({'error':'you do not have permission to perform this action'}, status = 400)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'updateUserDetails':serializer.data})
    
class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({'error':'You do not have permission to perform this action'}, status = 400)
        self.perform_destroy(instance)
        return Response({'message':'User deleted successfully!'})
    

class ChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if new_password != confirm_password:
                return Response({'error':'new password and confirm password doesnot match'}, status=400)
            
            if request.user != user:
                return Response({'error':'you do not have permission to perform this action'}, status=400)
            
            if new_password and confirm_password == current_password:
                return Response({'error':'new password and current password cannot be same'}, status=400)
            
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                AccessToken.objects.filter(user=user).delete()
                
                return Response({'error':'password updated successfully!'}, status=400)
            else:
                return Response({'error':'Invalid password please try again!'}, status = 400)
        else:
            return Response({'error':'current password, new password and confirm password are required'}, status=400)
                
class UserFollowersRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowersListSerializer
    # permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'userDetails':serializer.data})
    
class UserFollowingRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowingsListSerializer
    # permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'userDetails':serializer.data})
#----------------------------------------------------------- AUTHENTICATION TOKENS -------------------------------------------------------------
class TokenViewClient(APIView):
    def get(self, request, *args, **kwargs):
        load_dotenv()
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(64))
        
        if Application.objects.filter(name = 'social_app').exists():
            token_object = Application.objects.filter(name = 'social_app')
            result_str = os.getenv('APP_CLIENT_SECRET')
        else:
            Application.objects.create(
                name = 'social_app',
                client_type = 'confidential',
                authorization_grant_type = 'password',
                client_secret = result_str
            )
            token_object = Application.objects.filter(name='social_app')
            
            with open('.env', 'a') as file:
                file.write(f'\n APP_CLIENT_SECRET={result_str}\n')
                
        client_id = token_object[0].client_id
        response_data = {
            'client_id':client_id,
            'client_secret':result_str
        }
        return Response({'clientDetails':response_data})
    
    
class ClientRefreshToken(APIView):
    
    def post(self, request, *args, **kwargs):
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret')
        refresh_token = request.data.get('refresh_token')
        
        url = f'{URL_SCHEME}://{request.get_host()}/o/token/'
        
        data_dict = {"grant_type":"refresh_token", "client_id":client_id, "client_secret":client_secret, "refresh_token":refresh_token}
        
        try:
            response = requests.post(url, data=data_dict)
            response_data = json.loads(response.text)
            
            access_token = response_data.get('access_token', '')
            refresh_token = response_data.get('refresh_token', '')
            
            response_data = {
                'tokens':{
                    'refresh_token':refresh_token,
                    'access_token':access_token,
                    'access_token_type': 'Bearer',
                }
            }
            return Response(response_data)
        except Exception as e:
            return Response({'error':str(e)}, status=500)
        
class UserLogin(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_class    = []
    required_scopes = [] 
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').lower()
        password = request.data.get('password')
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret')
        
        user = authenticate(request, email=email, password = password)
        if user is None:
            return Response({'error':'invalid credentials'}, status=400)
        
        devices = devices_for_user(user, confirmed=True)
        totp_devices = [device for device in devices if isinstance(device, TOTPDevice)]
        if totp_devices:
            return Response({'status':'2FA enabled', 'user_id':user, 'confirmed':True}, status=400)
        
        AccessToken.objects.filter(user=user.id).delete()
        RefreshToken.objects.filter(user=user.id).delete()
        
        url = f'{URL_SCHEME}://{request.get_host()}/o/token/'
        data_dict = {"grant_type":"password", "email":email, "password":password, "client_id":client_id, "client_secret":client_secret }
        response = requests.post(url, data=data_dict)
        response_data = json.loads(response.text)
        access_token = response_data.get('access_token', '')
        refresh_token = response_data.get('refresh_token', '')
        
        if not request.user_agent.browser.family == "Python Requests" and not request.user_agent.browser.family == "PostmanRuntime":            
            user_login_logs = UserLoginLogs.objects.create(
                user_id = user,
                browser = f'{request.user_agent.browser.family} {request.user_agent.browser.version_string}',
                operating_system = f'{request.user_agent.os.family} {request.user_agent.os.version_string}',
                device = request.user_agent.device.family,
                last_login = timezone.now(),
                ip_address = get_ip_address(request)
            )
        
        response_data = {
            'tokens':{
            'refresh_token':refresh_token,
            'access_token':access_token,
            'access_token_type':'Bearer',
            },
            'userDetails': {
                'id':user.id,
                'salutation_id': user.salutation_id.id if user.salutation_id else None,
                'salutation_name': user.salutation_id.name if user.salutation_id else None,
                'title_id': user.title_id.id if user.title_id else None,
                'title_name':user.title_id.name if user.title_id else None,
                'email': user.email,
                'username': user.username,
                'firstname':user.firstname,
                'lastname': user.lastname,
                'is_admin': user.is_admin,
                'last_login':user.last_login,
                'profile_photo': request.build_absolute_uri(user.profile_photo.url) if user.profile_photo else None,
                'confirmed':user.confirmed,
                                
            }
        }
        return Response(response_data)
    
class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        access_token =AccessToken.objects.get(user=request.user)
        access_token.delete()
        return Response({'message':'Logged out successfully!'})
      
#---------------------------------------------- TWO FACTOR AUTHENTICATION ------------------------------------------------------------------------
class GenerateRecoveryCodes(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            if request.user != user:
                return Response({'error':'you do not have permission to perform this action'}, status=400)
            totp_devices = devices_for_user(user, confirmed=True)
            totp_device = next((device for device in totp_devices if isinstance(device, TOTPDevice)), None)

            if not totp_device:
                return Response({'error': '2FA is not enabled'}, status=400)

            recovery_codes, created = RecoveryCode.objects.get_or_create(user=user)
            codes = recovery_codes.codes
            
            if not codes or len(codes)<10:
                existing_codes = recovery_codes.codes.copy()
                
                existing_codes = [code for code in existing_codes if not code.startswith("USED")]
                
                num_existing_codes = len(existing_codes)
                num_new_codes = 10 - num_existing_codes
                new_codes = generate_unique_recovery_codes(user, existing_codes, count=num_new_codes)
                recovery_codes.codes.extend(new_codes)
                recovery_codes.save()
                
                codes = recovery_codes.codes
                return Response({'recoveryCodes':codes})
        except Exception as e:
            return Response({'error':str(e)}, status=400)


class Enable2FA(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            if request.user != user:
                return Response({'error':'you do not have permission to perform this action'}, status=400)
            
            totp_devices = devices_for_user(user, confirmed=True)
            totp_device = next((device for device in totp_devices if isinstance(device, TOTPDevice)), None)
            
            if totp_device:
                return Response({'error':'2FA already enabled for this user'}, status =400)
            
            device = TOTPDevice.objects.create(user=user, name=user.name)
            qr_code = qrcode.QRCODE()
            qr_code.add_data(device.config_url)
            qr_code.make(fit=True)
            qr_code_image = qr_code.make_image()
            qr_code_buffer = BytesIO()
            qr_code_image.save(qr_code_buffer, format='PNG')
            qr_code_buffer.seek(0)
            qr_code_data = qr_code_buffer.getvalue()
            qr_code_data_uri = 'data:image/png;base64' + base64.b64encode(qr_code_data).decode('utf-8')
            return Response({'qrCode':qr_code_data_uri})
        except Exception as e:
            return Response({'error':str(e)}, status=400)
        
        
class Verify2FA(APIView):
    
    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        recovery_code = request.data.get('recovery_code')
        user = User.objects.get(id=id)
        totp_devices = devices_for_user(user, confirmed=True)
        totp_device = next((device for device in totp_devices if isinstance(device, TOTPDevice)), None)
        
        if not otp and not recovery_code:
            return Response({'error':'OTP or Recovery code is required'}, status=400)
        
        if not totp_device:
            return Response({'error':'2FA not enabled for this user'}, status=400)
        
        is_verified = totp_device.verify_token(otp)
        if is_verified:
            return Response({'message':'OTP verified successfully!'})
        
        if recovery_code:
            recovery_codes = RecoveryCode.objects.filter(user=user).exists()
            if recovery_codes and recovery_code in recovery_codes.codes:
                recovery_codes.codes.remove(recovery_code)
                recovery_codes.save()
                return Response({'message':'Recoverycode verified successfully!'})
        return Response({'error':'Invalid OTP or Recovery code'}, status=400)
        
        
class LoginAfterVerify(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        password = request.data.get('password')
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret')
        
        user = authenticate(request, email=username, password=password)
        
        if user is None:
            return Response({'status_code':606, 'error':'Invalid Credentials'}, status = 500)
        
        
    
        totp_devices = devices_for_user(user, confirmed=True)
        totp_device = next((device for device in totp_devices if isinstance(device, TOTPDevice)), None)
        if not totp_device:
            return Response({'error':'2FA is not enabled for this user'}, status=500)
        
        AccessToken.objects.filter(user=user.id).delete()
        RefreshToken.objects.filter(user=user.id).delete()    
        
        user.last_login = timezone.now()
        user.save()   
        url = f'{URL_SCHEME}://{request.get_host()}/o/token/'
        
        data_dict = {"grant_type":"password", "username":username, "password":password, "client_id":client_id, "client_secret":client_secret }
        aa = requests.post(url, data=data_dict)
        data = json.loads(aa.text)
        access_token = data.get('access_token', '')
        refresh_token = data.get('refresh_token', '')
        
        response_data = {
            'tokens':{
            'refresh_token':refresh_token,
            'access_token':access_token,
            'access_token_type':'Bearer',
            },
            'userDetails': {
                'id':user.id,
                'salutation_id': user.salutation_id.id if user.salutation_id else None,
                'salutation_name': user.salutation_id.name if user.salutation_id else None,
                'title_id': user.title_id.id if user.title_id else None,
                'title_name':user.title_id.name if user.title_id else None,
                'email': user.email,
                'username': user.username,
                'firstname':user.firstname,
                'lastname': user.lastname,
                'is_admin': user.is_admin,
                'profile_photo': request.build_absolute_uri(user.profile_photo.url) if user.profile_photo else None,
                'confirmed':True,
            
            }
        }
        return Response(response_data)
    
class Disable2FA(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if request.user != user:
                return Response({'error':'You do not have permission to perform this action'}, status=400)
        except User.DoesNotExist:
            return Response({'error':'user doesnot exists'}, status=400)
        
        totp_devices = devices_for_user(user, is_confirmed=True)
        for device in totp_devices:
            device.confirmed = False
            device.save()
        return Response({'message':'2FA disabled successfully!'})
    
#------------------------------------------------------------------ LOGIN LOGS -----------------------------------------------------------------

class UserLoginLogsByUser(generics.RetrieveAPIView):
    queryset = UserLoginLogs.objects.all()
    serializer_class = UserLoginLogSerializer
    permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = User.objects.filter(pk=user_id)
        queryset = self.get_queryset(user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'userLogs':serializer.data})
    
#------------------------------------------------- FOLLOW USERS ----------------------------------------------------------------------------
class UserFollowCreate(generics.CreateAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        following_id = request.data.get('following')
        user = User.objects.get(pk=following_id)
        request_status = request.data.get('request_status')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request_status:
            if user.is_private_account == True:
                request_status = 'pending'
            else:
                request_status = 'approved'
            request_status.save()
        serializer.save()
        return Response({'userFollowDetails':serializer.data})
 
    
    def list(self, request, *args, **kwargs):
        follower = self.kwargs.get('follower')
        followers = FollowUser.objects.filter(follower=follower, request_status='approved')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'userFollowingList':serializer.data})
    
    
    
#----------------------------------------------------------------- USER BLOCKS -----------------------------------------------------------------

class CreateUserBlock(generics.CreateAPIView):
    serializer_class = UserBlockSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'userBlock':'user blocked successfully!'})
    
class UserUnblock(generics.DestroyAPIView):
    queryset = BlockUser.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.blocked_by_user:
            return Response({'error':'you do not have permission to perform this action'}, status=400)
        self.perform_destroy(instance)
        return Response({'userBlock':'user unblocked successfully!'})
            