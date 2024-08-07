from rest_framework import serializers
from .models import *

class SupportContactSerializer(models.ModelSerializer):
    class Meta:
        model = SupportContact
        fields = '__all__'
        

class ReportOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportOption
        fields = '__all__'
        
class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = '__all__'
        
class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = '__all__'
        
class ReportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportUser
        fields = '__all__'