from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index),
    path(r'<int:num>/',views.detail),
    path(r'login/',views.login),
    path(r'user/login/',views.login),
    path(r'user/',views.user,name="user"),
    path(r'myself/',views.myself,name="myself"),
    #打卡签到
    path(r'user/signIn/',views.signIn,name="signIn"),
    #工作安排
    path(r'user/workArrangements/',views.workArrangements,name="workArrangements"),
    #加班
    path(r'user/workOvertime/',views.workOvertime,name="workOvertime"),
    #请假
    path(r'user/leaveWork/',views.leaveWork,name="leaveWork"),
    #个人信息
    path(r'user/selfInfo/',views.selfInfo,name="selfInfo"),
    #个人信息修改
    path(r'user/selfInfo/edit/',views.selfInfoEdit),
    path(r'user/selfInfo/sub/',views.generate_qrcode,name='qrcode'),
    path(r'qrform/',views.qrform,name='qrform'),
    path(r'qrform/signIn/',views.signIn),
    #个人信息修改提交
    path(r'user/selfInfo/edit/editSub/',views.editSub,name='editSub'),
    #请假、销假申请提交
    path(r'user/leaveWork/leaveSub/',views.leaveSub,name='leaveSub'),
    #加班申请提交
    path(r'user/workOvertime/overSub/',views.overSub,name='overSub'),
    #批准请假、销假
    path(r'user/approval/',views.approval,name='approval'),
    #请教、销假批准提交
    path(r'user/approval/arovalSub',views.approvalSub,name='approvalSub'),
    #经理管理员工信息
    path(r'user/userDetails',views.userDetails,name='userDetails'),
    #经理修改单个员工信息的edit键
    re_path(r'user/memberEdit(\d+)/',views.singleEdit,name='singleEdit'),
    #经理修改员工信息提交
    re_path(r'user/memberEdit/singleEditSub',views.singleEditSub,name='singleEditSub'),
    #经理删除员工信息
    re_path(r'user/memberDel(\d+)/',views.singleDel,name='singleDel'),
    #添加员工
    path(r'user/memberAdd/',views.singleAdd,name='singleAdd'),
    #经理添加员工信息提交
    re_path(r'user/memberAdd/singleAddSub',views.singleAddSub,name='singleAddSub'),
    #设置主管
    re_path(r'user/memberSet(\d+)/', views.singleSet, name='singleSet'),
    #主管修改单个工作班次的edit键
    re_path(r'user/workArrangements/arrangeEdit(\d+)/', views.arrangeEdit, name='arrangeEdit'),
    #主管修改工作班次提交
    re_path(r'user/workArrangements/arrangeEdit/arrangeEditSub',views.arrangeEditSub,name='arrangeEditSub'),
    #主管删除工作班次
    re_path(r'user/workArrangements/arrangeDel(\d+)/',views.arrangeDel,name='arrangeDel'),
    #批量删除
    path(r'user/workArrangements/selectDel/',views.selectDel,name='selectDel'),
    #批量删除提交
    path(r'user/workArrangements/selectDelSub/',views.selectDelSub,name='selectDelSub'),
    #工作安排
    path(r'user/workAttendances/',views.workAttendances,name="workAttendaces"),
    #员工信息
    path(r'user/detailInfos/',views.detailInfos,name="detailInfos"),
    #创建加班
    path(r'user/approval/overAdd/',views.overAdd,name='overAdd'),
    #创建加班提交
    path(r'user/approval/overAdd/overAddSub',views.overAddSub,name='overAddSub'),
]
