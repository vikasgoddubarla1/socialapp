from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .functions import *
# Create your views here.


class CreateSupportTicket(generics.CreateAPIView):
    serializer_class = SupportContact
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'supportDetails':serializer.data})
    
class UpdateSupportTicket(generics.UpdateAPIView):
    queryset = SupportContact.objects.all()
    serializer_class = SupportContact
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'supportDetails':'Support details has been updated'})
    
class GetSupportTickets(generics.RetrieveAPIView):
    queryset = SupportContact.objects.all()
    serializer_class = SupportContact
    permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs.get('created_by')
        queryset = self.filter_queryset(created_by=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'supportTickets':serializer.data})
    
class DeleteSupportTickets(generics.DestroyAPIView):
    queryset = SupportContact.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_admin:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'supportTicketDetails':'support ticket deleted successfully!'})
    
#------------------------------------------------------- REPORTS -------------------------------------------------------------------------------


class CreateReportOption(generics.CreateAPIView):
    serializer_class = ReportOptionSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({'error':'you do not have permission to perform this action'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'supportDetails':serializer.data})
    
class DeleteReportOptions(generics.DestroyAPIView):
    queryset = ReportOption.objects.all()
    serializer_class = ReportOptionSerializer
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_admin:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'supportTicketDetails':'report option deleted successfully!'})
    
#------------------------------------------------ POST REPORTS -------------------------------------------------------------------------------
class CreatePostReports(generics.CreateAPIView):
    serializer_class = PostReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'supportDetails':serializer.data})
    

class UpdatePostReports(generics.UpdateAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'supportDetails':'Post report details has been updated'})
    
class DeletePostReports(generics.DestroyAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_admin:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'supportTicketDetails':'Post report deleted successfully!'})
    
class GetPostReports(generics.RetrieveAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        queryset = self.filter_queryset(post_id=post_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'supportTickets':serializer.data})
    

#------------------------------------------------------- COMMENT REPORTS -----------------------------------------------------------------------
class CreateCommentReports(generics.CreateAPIView):
    serializer_class = CommentReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'supportDetails':serializer.data})
    
class UpdateCommentReports(generics.UpdateAPIView):
    queryset = CommentReport.objects.all()
    serializer_class = CommentReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'supportDetails':'post comment report details has been updated'})
    
class DeletePostCommentReports(generics.DestroyAPIView):
    queryset = CommentReport.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_admin:
            return Response({'error':'You do not have permission to perform this action'}, status=400)
        instance.delete()
        return Response({'supportTicketDetails':'Post report deleted successfully!'})
    
class GetPostCommentReports(generics.RetrieveAPIView):
    queryset = CommentReport.objects.all()
    serializer_class = CommentReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def retrieve(self, request, *args, **kwargs):
        post_comment_id = self.kwargs.get('post_comment_id')
        queryset = self.filter_queryset(post_comment_id=post_comment_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'supportTickets':serializer.data})