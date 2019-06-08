from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path(r'<int:num>/',views.detail),
    path(r'login/',views.login),
    path(r'user/login/',views.login),
    path(r'user/',views.user,name="user"),
    path(r'myself/',views.myself,name="myself"),
    path(r'user/signIn/',views.signIn,name="signIn"),
    path(r'user/workArrangements/',views.workArrangements,name="workArrangements"),
    path(r'user/selfInfo/',views.selfInfo,name="selfInfo"),
    path(r'user/selfInfo/edit/',views.selfInfoEdit),
    path(r'user/selfInfo/sub/',views.generate_qrcode,name='qrcode'),
    path(r'qrform/',views.qrform,name='qrform'),
    path(r'qrform/signIn/',views.signIn),
    path(r'user/selfInfo/edit/editSub/',views.editSub,name='editSub'),
]
