
from django.urls import path
from .views import *

urlpatterns = [
    path('supportTicket/list', GetSupportTickets.as_view(), name='support-ticket-list'),
    path('supportTicket/create', CreateSupportTicket.as_view(), name='support-ticket-create'),
    path('supportTicket/update/<int:pk>', UpdateSupportTicket.as_view(), name='support-ticket-update'),
    path('supportTicket/delete/<int:pk>', DeleteSupportTickets.as_view(), name='support-ticket-delete'),
    
    #--------------------------------------- REPORT OPTIONS -------------------------------------------
    path('reportOption/create', CreateReportOption.as_view(), name='report-option-create'),
    path('reportOption/delete/<int:pk>', DeleteReportOptions.as_view(), name='report-option-delete'),
    
    #----------------------------------------- POST REPORTS ---------------------------------------------
    path('postReport/create', CreatePostReports.as_view(), name='report-post-create'),
    path('postReport/update/<int:pk>', UpdatePostReports.as_view(), name='report-post-update'),
    path('postReport/delete/<int:pk>', DeletePostReports.as_view(), name='report-post-delete'),
    path('postReport/list/<int:post_id>', GetPostReports.as_view(), name='report-post-list'),
    
    
    #-------------------------------------COMMENT REPORTS -----------------------------------------
    
    path('commentReport/create', CreateCommentReports.as_view(), name='report-comment-create'),
    path('postReport/update/<int:pk>', UpdateCommentReports.as_view(), name='report-comment-update'),
    path('postReport/delete/<int:pk>', DeleteCommentReports.as_view(), name='report-comment-delete'),
    path('postReport/list/<int:post_comment_id>', GetCommentReports.as_view(), name='report-comment-list'),
    
    
    
]
