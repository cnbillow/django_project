from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('<int:num>/',views.detail),
    path('login/',views.login),
    path('user/login/',views.login),
    path('user/',views.user,name="user"),
    path('myself/',views.myself,name="myself"),
    path('user/signIn/',views.signIn,name="signIn"),
    path(r'user/selfInfo/',views.selfInfo,name="selfInfo"),
    path(r'user/selfInfo/sub/',views.generate_qrcode,name='qrcode'),
    path(r'qrform/',views.qrform,name='qrform'),
    path(r'qrform/signIn/',views.signIn),
]
