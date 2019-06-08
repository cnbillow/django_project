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
        userList = employees.objects.all()
        flag = 0
        userNow=None
        for userOne in userList:
            if (idGet == str(userOne.id)):
                if (passwordGet == userOne.password):
                    userNow=userOne
                    flag = 1
                    break
        if (flag == 1):
            rep = render(request, 'myAPP/webhtml/myself.html', {"user": userNow})
            rep.set_cookie("id",userNow.id)
            return rep
        else:
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
    userList = employees.objects.all()
    userNow = None
    for userOne in userList:
        if (employeeId == userOne.id):
            userNow = userOne
            break
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
    userList = employees.objects.all()
    userNow = None
    for userOne in userList:
        if (employeeId == userOne.id):
            userNow = userOne
            break
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
    userList = employees.objects.all()
    userNow = None
    for userOne in userList:
        if (employeeId == userOne.id):
            userNow = userOne
            break
    print(userNow.name)
    return render(request,'myAPP/webhtml/selfInfoEdit.html', {"user": userNow})

@csrf_exempt
def editSub(request):
    nameGet=''
    if request.method == 'post':
        employeeId = int(request.COOKIES["id"])
        userList = employees.objects.all()
        userNow = None
        for userOne in userList:
            if (employeeId == userOne.id):
                userNow = userOne
                break
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
    userList = arrangements.objects.all()
    userNow = []
    for userOne in userList:
        if (employeeId == userOne.employee_id):
            userNow.append(userOne)
    #userArrangement=
    #print(userNow[0].day)
    return render(request,'myAPP/webhtml/workArrangements.html', {"userArr": userNow})