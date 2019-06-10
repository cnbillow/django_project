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
                    print("#####")
                    break
        if (flag == 1):
            print("#######")
            rep = render(request, 'myAPP/webhtml/myself.html', {"id": idGet})
            rep.set_cookie("id",idGet,path='/',secure=True)

            return rep
        else:
            return render(request, 'myAPP/errorFalse.html')


@csrf_exempt
def user(request):
    if request.method == "GET":
        return render(request, 'myAPP/login.html')
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
            # userList = employees.objects.all()
            # flag = 0
            # userNow=None
            #
            # for userOne in userList:
            #     if (idGet == str(userOne.id)):
            #         if (passwordGet == userOne.password):
            #             userNow=userOne
            #             flag = 1
            #             break
            # if (flag == 1):

        elif(typeGet == 1):
            try:
                userNow=departments.objects.get(employee_id=idGet)
                userNow=employees.objects.get(id=idGet,password=passwordGet)
                rep = render(request, 'myAPP/webhtml/supervisorMyself.html', {"user": userNow})
                rep.set_cookie("id", userNow.id)
                rep.set_cookie("type", typeGet)
                return rep
            except:
                return render(request, 'myAPP/errorFalse.html')
        else:
            try:
                userNow=managers.objects.get(id=idGet,password=passwordGet)
                rep = render(request, 'myAPP/webhtml/managerMyself.html', {"user": userNow})
                rep.set_cookie("id", userNow.id)
                rep.set_cookie("type", typeGet)
                return rep
            except:
                return render(request, 'myAPP/errorFalse.html')


def myself(request):
    return render(request,'myAPP/webhtml/myself.html')

@csrf_exempt
def signIn(request):
    id=attendances.objects.all().count()
    employeeId = int(request.COOKIES['id'])
    getTime=time.localtime(time.time())
    getYear=getTime[0]
    getMonth=getTime[1]
    getDay=getTime[2]
    getHour=getTime[3]
    getMinute=getTime[4]
    timeAt=str(getYear)+'-'+str(getMonth)+'-'+str(getDay)+'-'+str(getHour)+':'+str(getMinute)
    userNow=employees.objects.get(id=employeeId)
    userName=userNow.name
    if(getHour>=8 and getHour<=11):
        try:
            sign_already=attendances.objects.get(employee_id=employeeId)
            return render(request,'myAPP/webhtml/signFalse.html')
        except BaseException:
            attendances.objects.create(id=id+1,name=userName, employee_id=employeeId,arrive_at=timeAt,is_overtime=0)
            return render(request,'myAPP/webhtml/signResult.html')
    elif(getHour>=14 and getHour<=17):
        try:
            employeeOne=attendances.objects.get(employee_id=employeeId)
            leaveAt=employeeOne.leave_at
            if(leaveAt!=""):
                return render(request, 'myAPP/webhtml/signFalse.html')
            else:
                employeeOne.leave_at = timeAt
                employeeOne.save()
                return render(request, 'myAPP/webhtml/signResult.html')
        except BaseException:
            attendances.objects.create(id=id + 1,name=userName, employee_id=employeeId, arrive_at=timeAt,leave_at=timeAt, is_overtime=0)
            return render(request, 'myAPP/webhtml/signResult.html')
    else:
        return render(request, 'myAPP/webhtml/signFalse.html')

def selfInfo(request):
    employeeId = int(request.COOKIES["id"])
    userNow = employees.objects.get(id=employeeId)
    return render(request,'myAPP/webhtml/selfInformation.html', {"user": userNow})


#二维码获取
import qrcode
from django.utils.six import BytesIO

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

def selfInfoEdit(request):
    employeeId = int(request.COOKIES["id"])
    userNow = employees.objects.get(id=employeeId)
    print(userNow.name)
    return render(request,'myAPP/webhtml/selfInfoEdit.html', {"user": userNow})

@csrf_exempt
def editSub(request):
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

def workArrangements(request):
    employeeId = int(request.COOKIES["id"])
    userNow=arrangements.objects.filter(employee_id=employeeId)
    return render(request,'myAPP/webhtml/workArrangements.html', {"userArr": userNow})

def leaveWork(request):
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


def workOvertime(request):
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

@csrf_exempt
def leaveSub(request):
    startGet = request.POST.get("startTime")
    endGet = request.POST.get("endTime")
    reasonGet = request.POST.get("reason")
    employeeId = int(request.COOKIES["id"])
    typeGet=request.POST.get("applicationType")
    id = leaves.objects.all().count()
    leaves.objects.create(id=id+1,employee_id_id=employeeId,type=typeGet,start_date=startGet,end_date=endGet,reason=reasonGet,status=0)
    return render(request,'myAPP/webhtml/workRight.html')

@csrf_exempt
def overSub(request):
    startGet = request.POST.get("startTime")
    endGet = request.POST.get("endTime")
    reasonGet = request.POST.get("reason")
    employeeId = int(request.COOKIES["id"])
    id = leaves.objects.all().count()
    print(startGet)
    overtimes.objects.create(id=id + 1, employee_id_id=employeeId, start_time=startGet, end_time=endGet,reason=reasonGet, status=0)
    return render(request, 'myAPP/webhtml/workRight.html')

@csrf_exempt
def approval(request):
    leaveList = leaves.objects.all()
    leavesArrange = leaves.objects.filter(status=0)
    return render(request,'myAPP/webhtml/approval.html',{"leaveInfos":leavesArrange})

@csrf_exempt
def approvalSub(request):
    num = 1
    while(1):
        try:
            statusGet=request.POST.get("info"+str(num))
            if(statusGet!=0 and statusGet!=None):
                changeStatus(num,statusGet)
            num=num+1
        except:
            break
    return render(request, 'myAPP/webhtml/workRight.html')

def changeStatus(num,status):
    leaveOne=leaves.objects.get(id=num)
    leaveOne.status=status
    leaveOne.save()

