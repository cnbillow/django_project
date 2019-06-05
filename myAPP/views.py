from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse
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
    employeeId = request.POST.get('id')
    try:
        sign_already=attendances.objects.get(employee_id=employeeId)
        return render(request,'myAPP/webhtml/signFalse.html')
    except BaseException:
        attendances.objects.create(id=id+1,employee_id=employeeId,arrive_at=0,is_overtime=0)
        return render(request,'myAPP/webhtml/signResult.html')

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