from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse
import time
def index(request):
    return render(request,'myAPP/login.html')
def detail(request,num):
    return HttpResponse(["softdesign is here:",num])

from .models import employees,departments,overtimes,arrangements,attendances,leaves,managers,temp_arrangements

#login并没有用到
@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'myAPP/login.html')
    else:
        idGet = request.POST.get("username")
        passwordGet = request.POST.get("password")
        userList = employees.objects.all()
        flag = 0
        for userOne in userList:
            if (idGet == userOne.name):
                if (passwordGet == userOne.password):
                    flag = 1
                    break
        if (flag == 1):
            rep = render(request, 'myAPP/webhtml/myself.html', {"id": idGet})
            rep.set_cookie("id",idGet,path='/',secure=True)

            return rep
        else:
            return render(request, 'myAPP/errorFalse.html')

#登录逻辑判断
@csrf_exempt
def user(request):
    if request.method == "GET":
        rep = render(request, 'myAPP/login.html')
        try:
            employeeId = int(request.COOKIES["id"])
            del request.COOKIES["id"]
            typeGet = int(request.COOKIES["type"])
            del request.COOKIES["type"]
            rep.delete_cookie("id")
            rep.delete_cookie("type")
        except:
            pass
        return rep
    else:
        idGet = request.POST.get("id")
        passwordGet = request.POST.get("password")
        typeGet = int(request.POST.get("userType"))
        if(typeGet == 0):
            try:
                userNow=employees.objects.get(id=idGet,password=passwordGet)
                rep = render(request, 'myAPP/webhtml/myself.html', {"user": userNow})
                rep.set_cookie("id", userNow.id)
                rep.set_cookie("type", typeGet)
                return rep
            except:
                return render(request, 'myAPP/errorFalse.html')
        elif(typeGet == 1):
            try:
                userNow=departments.objects.get(employee_id=idGet)
                userNow=employees.objects.get(id=idGet,password=passwordGet)
                num=leaves.objects.filter(status=0).count()
                rep = render(request, 'myAPP/webhtml/supervisorMyself.html', {"user": userNow,"noticesNum":num})
                rep.set_cookie("id", userNow.id)
                rep.set_cookie("type", typeGet)
                return rep
            except:
                return render(request, 'myAPP/errorFalse.html')
        else:
            try:
                userNow=managers.objects.get(id=idGet,password=passwordGet)
                num = overtimes.objects.filter(status=0).count()
                rep = render(request, 'myAPP/webhtml/managerMyself.html', {"user": userNow,"noticesNum":num})
                rep.set_cookie("id", userNow.id)
                rep.set_cookie("type", typeGet)
                return rep
            except:
                return render(request, 'myAPP/errorFalse.html')

#用于页面跳转
def myself(request):
    if(isLognIn(request)==1):
        typeGet = int(request.COOKIES["type"])
        if(typeGet==0):
            return render(request,'myAPP/webhtml/myself.html')
        elif(typeGet==1):
            num = leaves.objects.filter(status=0).count()
            return render(request, 'myAPP/webhtml/supervisorMyself.html',{"noticesNum":num})
        else:
            num = overtimes.objects.filter(status=0).count()
            return render(request, 'myAPP/webhtml/managerMyself.html',{"noticesNum":num})
    else:
        return render(request,'myAPP/login.html')

#用于打卡
@csrf_exempt
def signIn(request):
    if(isLognIn(request)==1):
        id=attendances.objects.all().count()
        employeeId = int(request.COOKIES['id'])
        getTime=time.localtime(time.time())
        getYear=getTime[0]
        getMonth=getTime[1]
        getDay=getTime[2]
        getHour=getTime[3]
        getMinute=getTime[4]
        idSet=str(getYear)+str(getMonth).zfill(2)+str(getDay).zfill(2)+str(employeeId)
        timeAt=str(getYear)+'-'+str(getMonth)+'-'+str(getDay)+'-'+str(getHour)+':'+str(getMinute)
        userNow=employees.objects.get(id=employeeId)
        userName=userNow.name
        if(getHour>=8 and getHour<=11):
            try:
                sign_already=attendances.objects.get(employee_id=employeeId,notice=idSet)
                return render(request,'myAPP/webhtml/signFalse.html')
            except:
                attendances.objects.create(id=id+1,notice=idSet,name=userName, employee_id=employeeId,arrive_at=timeAt,is_overtime=0)
                return render(request,'myAPP/webhtml/signResult.html')
        elif(getHour>=14 and getHour<=24):
            try:
                employeeOne=attendances.objects.get(employee_id=employeeId,notice=idSet)
                leaveAt=employeeOne.leave_at
                if(leaveAt!=""):
                    return render(request, 'myAPP/webhtml/signFalse.html')
                else:
                    employeeOne.leave_at = timeAt
                    employeeOne.save()
                    return render(request, 'myAPP/webhtml/signResult.html')
            except:
                attendances.objects.create(id=id+1,notice=idSet,name=userName, employee_id=employeeId, arrive_at=timeAt,leave_at=timeAt, is_overtime=0)
                return render(request, 'myAPP/webhtml/signResult.html')
        else:
            return render(request, 'myAPP/webhtml/signFalse.html')
    else:
        return render(request, 'myAPP/login.html')

#查看个人信息
def selfInfo(request):
    if(isLognIn(request)==1):
        employeeId = int(request.COOKIES["id"])
        userNow = employees.objects.get(id=employeeId)
        return render(request,'myAPP/webhtml/selfInformation.html', {"user": userNow})
    else:
        return render(request, 'myAPP/login.html')

#二维码获取
import qrcode
from django.utils.six import BytesIO

#生成打卡二维码，暂时不用
def generate_qrcode(request):
    website = request.POST.get('website')
    if (len(website) != 0):
        img = qrcode.make(str(website))
        buf = BytesIO()
        img.save(buf)
        image_stream = buf.getvalue()
        response = HttpResponse(image_stream, content_type="image/png")
        return response
    return HttpResponse(u"网址不能为空！")

def qrform(request):
    return render(request,'myAPP/qrform.html')

#修改个人信息
def selfInfoEdit(request):
    if(isLognIn(request)==1):
        employeeId = int(request.COOKIES["id"])
        userNow = employees.objects.get(id=employeeId)
        return render(request,'myAPP/webhtml/selfInfoEdit.html', {"user": userNow})
    else:
        return render(request, 'myAPP/login.html')

#个人信息修改后提交
@csrf_exempt
def editSub(request):
    if(isLognIn(request)==1):
        if request.method == 'post':
            employeeId = int(request.COOKIES["id"])
            userNow = employees.objects.get(id=employeeId)
            nameGet = request.POST.get("name")
            birthdayGet = request.POST.get("birthday")
            userNow.name=nameGet
            userNow.birthday=birthdayGet
            userNow.save()
            return render(request, 'myAPP/webhtml/signResult.html')
        else:
            return render(request, 'myAPP/webhtml/signFalse.html')
    else:
        return render(request, 'myAPP/login.html')

#查看工作班次
def workArrangements(request):
    if(isLognIn(request)==1):
        employeeId = int(request.COOKIES["id"])
        userNow=arrangements.objects.filter(employee_id=employeeId)
        return render(request,'myAPP/webhtml/workArrangements.html', {"userArr": userNow})
    else:
        return render(request,'myAPP/login.html')

#请假销假页面
def leaveWork(request):
    if(isLognIn(request)==1):
        employeeId = int(request.COOKIES["id"])
        userNow = employees.objects.get(id=employeeId)
        userLeave = leaves.objects.all()
        leaveInfo = []
        for leaveOne in userLeave:
            if (employeeId == leaveOne.employee_id_id):
                leaveInfo.append(leaveOne)
        if(len(leaveInfo)>=3):
            return render(request, 'myAPP/webhtml/leaveWorkApplication.html', {"user": userNow, "leave": leaveInfo[-3:]})
        else:
            return render(request, 'myAPP/webhtml/leaveWorkApplication.html', {"user": userNow, "leave": leaveInfo})
    else:
        return render(request, 'myAPP/login.html')

#加班页面
def workOvertime(request):
    if(isLognIn(request)==1):
        employeeId = int(request.COOKIES["id"])
        userNow = employees.objects.get(id=employeeId)
        overInfo = []
        userOver = overtimes.objects.all()
        for overOne in userOver:
            if (employeeId == overOne.employee_id_id):
                overInfo.append(overOne)
        if(len(overInfo)>=3):
            return render(request, 'myAPP/webhtml/workOvertimeApplication.html', {"user": userNow, "over": overInfo[-3:]})
        else:
            return render(request, 'myAPP/webhtml/workOvertimeApplication.html', {"user": userNow, "over": overInfo})
    else:
        return render(request, 'myAPP/login.html')

#请假提交
@csrf_exempt
def leaveSub(request):
    if(isLognIn(request)==1):
        startGet = request.POST.get("startTime")
        endGet = request.POST.get("endTime")
        reasonGet = request.POST.get("reason")
        employeeId = int(request.COOKIES["id"])
        typeGet=request.POST.get("applicationType")
        id = leaves.objects.all().count()
        leaves.objects.create(id=id+1,employee_id_id=employeeId,type=typeGet,start_date=startGet,end_date=endGet,reason=reasonGet,status=0)
        return render(request,'myAPP/webhtml/workRight.html')
    else:
        return render(request, 'myAPP/login.html')

#加班提交
@csrf_exempt
def overSub(request):
    if(isLognIn(request)==1):
        startGet = request.POST.get("startTime")
        endGet = request.POST.get("endTime")
        reasonGet = request.POST.get("reason")
        employeeId = int(request.COOKIES["id"])
        id = overtimes.objects.all().count()
        overtimes.objects.create(id=id + 1, employee_id_id=employeeId, start_time=startGet, end_time=endGet,reason=reasonGet, status=0)
        return render(request, 'myAPP/webhtml/workRight.html')
    else:
        return render(request, 'myAPP/login.html')

#审批页面
@csrf_exempt
def approval(request):
    if(isLognIn(request)==1):
        typeGet = int(request.COOKIES["type"])
        if (typeGet == 1):
            leavesArrange = leaves.objects.filter(status=0)
            return render(request,'myAPP/webhtml/approval.html',{"leaveInfos":leavesArrange,"type":typeGet})
        elif(typeGet == 2):
            oversArrange = overtimes.objects.filter(status=0)
            return render(request,'myAPP/webhtml/approval.html',{"leaveInfos":oversArrange,"type":typeGet})
        else:
            return render(request,'myAPP/webhtml/workFalse.html')
    else:
        return render(request,'myAPP/login.html')

#审批提交
@csrf_exempt
def approvalSub(request):
    if(isLognIn(request)==1):
        typeGet = int(request.COOKIES["type"])
        if(typeGet==1):
            leavesList=leaves.objects.all()
            num=1
            for i in leavesList:
                if(i.status==0):
                    break
                else:
                    num=num+1
        elif(typeGet==2):
            oversList = overtimes.objects.all()
            num = 1
            for i in oversList:
                if (i.status == 0):
                    break
                else:
                    num = num + 1
        else:
            num=1
        while(1):
            try:
                statusGet=request.POST.get("info"+str(num))
                if(statusGet == None):
                    break
                elif(statusGet!=0):
                    changeStatus(num,statusGet,typeGet)
                num=num+1
            except:
                break
        return render(request, 'myAPP/webhtml/workRight.html')
    else:
        return render(request, 'myAPP/login.html')


#经理查看全体员工的信息
def userDetails(request):
    if(isLognIn(request)==1):
        employeesList=employees.objects.all()
        return render(request, 'myAPP/webhtml/employeesInfo.html', {"employeesInfos": employeesList})
    else:
        return render(request,'myAPP/login.html')

#编辑弹窗
def singleEdit(request,arg):
    if (isLognIn(request) == 1):
        idGet=int(arg)
        employeeOne=employees.objects.get(id=idGet)
        return render(request, 'myAPP/webhtml/memberEdit.html',{"employee":employeeOne})
    else:
        return render(request,'myAPP/login.html')

def arrangeEdit(request,arg):
    if (isLognIn(request) == 1):
        idGet=int(arg)
        employeeOne=arrangements.objects.get(id=idGet)
        return render(request, 'myAPP/webhtml/arrangeEdit.html',{"employee":employeeOne})
    else:
        return render(request,'myAPP/login.html')

def selectDel(request):
    if (isLognIn(request) == 1):
        return render(request, 'myAPP/webhtml/selectDel.html')
    else:
        return render(request,'myAPP/login.html')

def selectDelSub(request):
    if (isLognIn(request) == 1):
        dayGet = request.POST.get("day")
        startIdGet = int(request.POST.get("startId"))
        endIdGet = int(request.POST.get("endId"))
        for num in range(startIdGet,endIdGet):
            try:
                arrangements.objects.get(day=dayGet,employee_id=num).delete()
            except:
                continue
        return render(request, 'myAPP/webhtml/workRight.html')
    else:
        return render(request, 'myAPP/login.html')

#删除弹窗
def singleDel(request,arg):
    if (isLognIn(request) == 1):
        employees.objects.get(id=int(arg)).delete()
        return render(request, 'myAPP/webhtml/workRight.html')
    else:
        return render(request,'myAPP/login.html')

def arrangeDel(request,arg):
    if (isLognIn(request) == 1):
        arrangements.objects.get(id=int(arg)).delete()
        return render(request, 'myAPP/webhtml/workRight.html')
    else:
        return render(request,'myAPP/login.html')

@csrf_exempt
def singleAdd(request):
    if (isLognIn(request) == 1):
        return render(request, 'myAPP/webhtml/memberAdd.html')
    else:
        return render(request,'myAPP/login.html')

#对任命主管的操作
def singleSet(request,arg):
    if (isLognIn(request) == 1):
        employeeOne=employees.objects.get(id=int(arg))
        employeeOld=employees.objects.get(department_id_id=employeeOne.department_id_id,isSupervisor=1)
        employeeOne.isSupervisor=1
        employeeOne.save()
        employeeOld.isSupervisor=0
        employeeOld.save()
        departmentOne=departments.objects.get(id=employeeOne.department_id_id)
        departmentOne.name=employeeOne.name
        departmentOne.employee_id=employeeOne.id
        departmentOne.save()
        return render(request, 'myAPP/webhtml/workRight.html')
    else:
        return render(request,'myAPP/login.html')

#弹窗的表单提交
@csrf_exempt
def singleEditSub(request):
    if(isLognIn(request)==1):
        oldIdGet=request.POST.get("oldId")
        employeeOne = employees.objects.get(id=oldIdGet)
        nameGet = request.POST.get("username")
        idGet = request.POST.get("userid")
        passwordGet = request.POST.get("password")
        departmentGet = request.POST.get("departmentid")
        employeeOne.name=nameGet
        employeeOne.id=idGet
        employeeOne.password=passwordGet
        employeeOne.department_id_id=departmentGet
        employeeOne.save()
        return render(request,'myAPP/webhtml/workRight.html')
    else:
        return render(request,'myAPP/login.html')

def arrangeEditSub(request):
    if (isLognIn(request) == 1):
        dayGet = request.POST.get("day")
        idGet = int(request.POST.get("id"))
        arrangeOne = arrangements.objects.get(employee_id=idGet,day=dayGet)
        startTimeAmGet = request.POST.get("startTimeAm")
        endTimeAmGet = request.POST.get("endTimeAm")
        startTimePmGet = request.POST.get("startTimePm")
        endTimePmGet = request.POST.get("endTimePm")
        arrangeOne.start_time_am=startTimeAmGet
        arrangeOne.end_time_am=endTimeAmGet
        arrangeOne.start_time_pm=startTimePmGet
        arrangeOne.end_time_pm=endTimePmGet
        arrangeOne.save()
        return render(request, 'myAPP/webhtml/workRight.html')
    else:
        return render(request, 'myAPP/login.html')

@csrf_exempt
def singleAddSub(request):
    nameGet = request.POST.get("username")
    idGet = request.POST.get("userid")
    passwordGet = request.POST.get("password")
    departmentGet = request.POST.get("departmentid")
    employees.objects.create(id=int(idGet),name=nameGet,password=passwordGet,department_id_id=int(departmentGet))
    return render(request,'myAPP/webhtml/workRight.html')

#验证登录状态
def isLognIn(request):
    try:
        employeeId = int(request.COOKIES["id"])
        typeGet = int(request.COOKIES["type"])
        return 1
    except:
        return 0

#审批用的修改申请状态
def changeStatus(num,status,typeGet):
    if(typeGet == 1):
        leaveOne=leaves.objects.get(id=num)
        leaveOne.status=status
        leaveOne.save()
        if(int(leaveOne.status)==1):
            startGet=leaveOne.start_time
            endGet=leaveOne.end_time
            startOne=arrangements.objects.get(employee_id=leaveOne.employee_id_id,day=startGet)
            endOne=arrangements.objects.get(employee_id=leaveOne.employee_id_id,day=endGet)
            startId=startOne.id
            endId=endOne.id
            for num in range(startId,endId):
                try:
                    arrangementGet=arrangements.objects.get(id=num,employee_id=leaveOne.employee_id_id)
                except:
                    continue
                arrangementGet.start_time_am='-'
                arrangementGet.end_time_am='-'
                arrangementGet.start_time_pm='-'
                arrangementGet.end_time_pm='-'
                arrangementGet.save()
    elif(typeGet == 2):
        overOne = overtimes.objects.get(id=num)
        overOne.status = status
        overOne.save()