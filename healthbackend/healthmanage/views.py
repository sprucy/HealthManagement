from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404 
from django.views.generic import View
from . import models
from . import forms
from .models import UserInfo,BodyInfo,SmokeDiabetesInfo,BloodPressure,Bcholesterin
import numpy as np
import datetime
from .risks import UserData,HealthRiskAssess,AnalyseStatistics
from django.contrib.admin import site
from django.views.decorators.csrf import csrf_exempt

# API View

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@csrf_exempt


# Create your views here.

def login(request):     
    if request.user.is_authenticated:  # 判断是否重复登录
        return redirect("/healthmanage/") 
    if request.method=='POST':        
        login_form = forms.UserLoginForm(request.POST)
        if login_form.is_valid():
            username=request.POST.get('username','')        
            password=request.POST.get('password','')        
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:            
                    auth.login(request, user)
                    return redirect("/healthmanage/")   
                else:
                    message='用户未激活,请与管理员联系！'
            else:
                message='用户不存在或密码错误！'
        else:
            message = login_form.errors  #获取form中定义的校验错误信息
    login_form = forms.UserLoginForm()        
    return render(request,"healthmanage/login.html",locals()) #locals把全部局部变量传给模板，这里主要传输的是message，也可以直接传

def register(request):   
    if request.user.is_authenticated:  # 不允许重复登录
        return redirect("/healthmanage/") 
    if request.method == 'POST':        
        regist_form = forms.UserRegistForm(request.POST)
        if regist_form.is_valid():
            username = request.POST.get('username')        
            password = request.POST.get('password')     
            password1 = request.POST.get('password1')     
            #username, email=None, password=None, **extra_fields
            if password != password1:
                message = '两次输入的密码不同！'
                return render(request,'healthmanage/register.html',locals())
            else: 
                if User.objects.filter(username=username).first():
                    message = '用户已存在！'
                    return render(request,'healthmanage/register.html',locals()) 
                else:
                    user = User.objects.create_user(username=username,password=password)       
                    if user:            
                        group = Group.objects.get(name='个人用户') 
                        group.user_set.add(user) 
                        auth.login(request, user) 
                        return redirect("/healthmanage/")  
                    else:
                        message = '用户注册失败，请与管理员联系！'
                        return render(request,'healthmanage/register.html',locals())
    regist_form = forms.UserRegistForm()
    return render(request,'healthmanage/register.html',locals())

def logout(request):
    auth.logout(request)
    return redirect('/healthmanage/login/')

@login_required
def icvdrisk(request):
    available_apps = site.get_app_list(request)
    user=request.user
    #平均值的天数
    avgnum=3
    userdata = UserData(user)
    sex = userdata.getsex()
    age = userdata.getage()
    myhealth = HealthRiskAssess()
    assessresult = myhealth.icvdassess(userdata)
    risks=[]
    intervents=[]
    val=''
    if userdata.getsmoke():
        val='吸烟'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))  
    if userdata.getdrink():
        val='饮酒'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))   
    if userdata.getdiabetes():
        val='糖尿病'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))    
    #体重
    bodyresult = userdata.getbodyinfoavg(avgnum)
    if assessresult:
        bmiresult = myhealth.bmiassess(bodyresult[3])
        assessresult.append(bmiresult)
        if (bmiresult == '体重偏瘦'):
            val='体重消瘦'
            risks = myhealth.getrisks(val)
            intervents = myhealth.getintervents(val)
        elif (bmiresult in ['体重偏胖','I度肥胖','II度肥胖','III度肥胖']):
            val='体重肥胖'
            risks.extend(myhealth.getrisks(val))
            intervents.extend(myhealth.getintervents(val))
    #血压
    bloodpressureresult = userdata.getbloodpressureavg(avgnum)
    if assessresult:
        bpresult = myhealth.bloodppressureassess(bloodpressureresult)
        if bpresult[0] == '收缩压较高' or bpresult[1] == '舒张压较高':
            val = '高血压' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == '收缩压较低' or bpresult[1] == '舒张压较低':
            val = '低血压' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val)) 
    #血脂
    bcholesterinresult = userdata.getbcholesterinavg(avgnum)
    if assessresult:
        bpresult = myhealth.bcholesterinassess(bcholesterinresult)
        if bpresult[0] == '总胆固醇较高':
            val = '高脂血' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == '总胆固醇较低':
            val = '低脂血' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
    if not val:
        risks =[['您拥有良好的日常习惯和身体条件，这是是身体健康的基础！']]
        intervents=[['建议保持良好的日常习惯，控制饮食，少盐少糖少油，同时加强体育锻炼!']]
    return render(request,'healthmanage/icvdrisk.html', locals())

@login_required
def weightassess(request):
    available_apps = site.get_app_list(request)    
    user = request.user
    #数据的天数
    num = 30
    #平均值的天数
    avgnum=3
    userdata = UserData(user)
    bddataset = userdata.getbodyinfo(num)
    sex = userdata.getsex()
    age = userdata.getage()
    assessresult = userdata.getbodyinfoavg(avgnum)
    myhealth = HealthRiskAssess()
    if assessresult:
        bmiresult = myhealth.bmiassess(assessresult[3])
        assessresult.append(bmiresult)
        risks=[]
        intervents=[]
        val=''
        if (bmiresult == '体重偏瘦'):
            val='体重消瘦'
            risks.extend(myhealth.getrisks(val))
            intervents.extend(myhealth.getintervents(val))
        elif (bmiresult in ['体重偏胖','I度肥胖','II度肥胖','III度肥胖']):
            val='体重肥胖'
            risks.extend(myhealth.getrisks(val))
            intervents.extend(myhealth.getintervents(val))
        else:
            risks.extend([['您的体重非常正常！'],])
            intervents.extend([['建议保持，同时加强体育锻炼']])
        normalweight = myhealth.getnormalweight(assessresult[0])
        normalwaist = myhealth.getnormalwaist(sex, assessresult[0])
    return render(request, 'healthmanage/weightassess.html', locals())

@login_required
def habitassess(request):
    available_apps = site.get_app_list(request)    
    user = request.user
    userdata = UserData(user)
    sex = userdata.getsex()
    age = userdata.getage()
    smokeyear = userdata.getsmokeyears()
    drinkyear = userdata.getdrinkyears()
    diabetesyear = userdata.getdiabetesyears()
    myhealth = HealthRiskAssess()
    risks=[]
    intervents=[]
    val=''
    if userdata.getsmoke():
        val='吸烟'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))  
    if userdata.getdrink():
        val='饮酒'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))   
    if userdata.getdiabetes():
        val='糖尿病'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))    
    if not val:
        risks =[['您日常没有吸烟和饮酒的习惯，也无糖尿病史，拥有良好的日常习惯是身体健康的基础！']]
        intervents=[['建议保持良好的日常习惯，控制饮食，少盐少糖少油，同时加强体育锻炼!']]
    return render(request, 'healthmanage/habitassess.html', locals())

@login_required
def bloodpressureassess(request):
    available_apps = site.get_app_list(request)    
    user = request.user
    #数据的天数
    num = 30
    #平均值的天数
    avgnum = 3
    userdata = UserData(user)
    bpdataset = userdata.getbloodpressure(num)
    assessresult = userdata.getbloodpressureavg(avgnum)
    if assessresult:
        myhealth = HealthRiskAssess()
        bpresult = myhealth.bloodppressureassess(assessresult)
        normaldbp = myhealth.getdbp()
        normalsbp = myhealth.getsbp()
        normalhr = myhealth.gethr()
        risks=[]
        intervents=[]
        val=''
        if bpresult[0] == '收缩压较高' or bpresult[1] == '舒张压较高':
            val = '高血压' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == '收缩压较低' or bpresult[1] == '舒张压较低':
            val = '低血压' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val)) 
        else:
            risks.extend([['祝贺您，您的血压正常，拥有良好的日常习惯是身体健康的基础！']])
            intervents.extend([['建议保持良好的日常习惯，控制饮食，少盐少糖少油，同时加强体育锻炼']])

        risks.extend(myhealth.getrisks(bpresult[2]))  
        intervents.extend(myhealth.getintervents(bpresult[2])) 
    return render(request, 'healthmanage/bloodpressureassess.html', locals())

@login_required
def bcholesterinassess(request):
    available_apps = site.get_app_list(request)    
    user = request.user
    #数据的天数
    num = 30
    #平均值的天数
    avgnum=3
    userdata = UserData(user)
    bsdataset = userdata.getbcholesterin(num)
    assessresult = userdata.getbcholesterinavg(avgnum)
    if assessresult:
        myhealth = HealthRiskAssess()
        bpresult = myhealth.bcholesterinassess(assessresult)
        normaltc = myhealth.gettc()
        normalldl = myhealth.getldl()
        normalhdl = myhealth.gethdl()
        normaltg = myhealth.gettg()
        risks=[]
        intervents=[]
        val=''
        if bpresult[0] == '总胆固醇较高':
            val = '高脂血' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == '总胆固醇较低':
            val = '低脂血' 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        else:
            riskstr=''
            if bpresult[1] == '低密度脂蛋白较低':
                riskstr += '您的'+bpresult[1]+'，注意加强低密度脂蛋白的摄入，'
            if bpresult[2] == '高密度脂蛋白较低':
                riskstr += '您的'+bpresult[2]+'，注意加强高密度脂蛋白的摄入，'
            if bpresult[3] == '甘油三酯较低':
                riskstr += '您的'+bpresult[3]+'，注意加强甘油三酯的摄入，'
            if bpresult[1] == '低密度脂蛋白较高':
                riskstr += '您的'+bpresult[1]+'，注意控制低密度脂蛋白的摄入，'
            if bpresult[2] == '高密度脂蛋白较高':
                riskstr += '您的'+bpresult[2]+'，注意控制高密度脂蛋白的摄入，'
            if bpresult[3] == '甘油三酯较高':
                riskstr += '您的'+bpresult[3]+'，注意控制甘油三酯的摄入，'
            riskstr += '拥有良好的日常习惯是身体健康的基础！'
            risks.extend([[riskstr]])    
            intervents.extend([['建议保持良好的生活习惯，控制饮食，加强体育锻炼！']])
    return render(request, 'healthmanage/bcholesterinassess.html', locals())

@login_required()
def index(request):
    available_apps = site.get_app_list(request)    
    user = request.user
    #数据的天数
    num = 30
    #平均值的天数
    avgnum=3
    userdata = UserData(user)
    bddataset = userdata.getbodyinfo(num)
    bpdataset = userdata.getbloodpressure(num)
    bsdataset = userdata.getbcholesterin(num)
    sex = userdata.getsex()
    age = userdata.getage()
    smokeyear = userdata.getsmokeyears()
    drinkyear = userdata.getdrinkyears()
    diabetesyear = userdata.getdiabetesyears()
    analyse = AnalyseStatistics()
    data = analyse.getusercount(sex=None, group='P')
    if data:
        dataset = analyse.convertdict(data)
        valmax = max([x[1] for x in data])
    return render(request, 'healthmanage/index.html', locals())

@permission_required( 'auth.view_user',  raise_exception=True)
def smokeanalye(request):
    available_apps = site.get_app_list(request)    
    analyse = AnalyseStatistics()
    data = analyse.getsmokecount(sex=None, group='P')
    if data:
        valmax = max([x[1] for x in data])
        dataset = analyse.convertdict(data)
    return render(request, 'healthmanage/smokeanalye.html', locals())

@permission_required('auth.view_user', raise_exception=True)
def drinkanalye(request):
    available_apps = site.get_app_list(request)    
    analyse = AnalyseStatistics()
    data = analyse.getdrinkcount(sex=None, group='P')
    if data:
        valmax = max([x[1] for x in data])
        dataset = analyse.convertdict(data)
    return render(request, 'healthmanage/drinkanalye.html', locals())

@permission_required('auth.view_user', raise_exception=True)
def fatanalye(request):
    available_apps = site.get_app_list(request)    
    analyse = AnalyseStatistics()
    data = analyse.getfatcount(sex=None, group='P')
    if data:
        valmax = max([x[1] for x in data])
        dataset = analyse.convertdict(data)
    return render(request, 'healthmanage/fatanalye.html', locals())

@permission_required('auth.view_user', raise_exception=True)
def diabetesanalye(request):
    available_apps = site.get_app_list(request)    
    analyse = AnalyseStatistics()
    data = analyse.getdiabetescount(sex=None, group='P')
    if data:
        valmax = max([x[1] for x in data])
        dataset = analyse.convertdict(data)
    return render(request, 'healthmanage/diabetesanalye.html', locals())

@permission_required('auth.view_user', raise_exception=True)
def hypertensionanalye(request):
    available_apps = site.get_app_list(request)    
    analyse = AnalyseStatistics()
    data = analyse.gethypertensioncount(sex=None, group='P')
    if data:
        valmax = max([x[1] for x in data])
        dataset = analyse.convertdict(data)
    return render(request, 'healthmanage/hypertensionanalye.html', locals())

@permission_required('auth.view_user', raise_exception=True)
def hyperlipemanalye(request):
    available_apps = site.get_app_list(request)    
    analyse = AnalyseStatistics()
    data = analyse.gethyperlipemcount(sex=None, group='P')
    if data:
        valmax = max([x[1] for x in data])
        dataset = analyse.convertdict(data)
    return render(request, 'healthmanage/hyperlipemanalye.html', locals())


@permission_required('auth.view_user', raise_exception=True)
def analye(request):
    available_apps = site.get_app_list(request)    
    user = request.user
    provinces = ['北京', '广东', '上海', '天津', '重庆', '辽宁', '江苏', '湖北', '四川', '陕西', '河北', '山西', '河南', '吉林',
        '黑龙江', '内蒙古', '山东', '安徽', '浙江', '福建', '湖南', '广西', '江西', '贵州', '云南', '西藏', '海南', '甘肃',
        '宁夏', '青海', '新疆', '香港', '澳门', '台湾']
    analyse = AnalyseStatistics()
    piedataset={}
    for province in provinces :
        piedataset[province] = [['男', 0, 0, 0, 0, 0], ['女', 0, 0, 0, 0, 0]]
    sex_choice = ('M', 'F')
    for sex in sex_choice:
        counts = analyse.getsmokecount(sex=sex, group='P')
        for count in counts:
            piedataset[count[0]][sex_choice.index(sex)][1] = count[1]
        counts = analyse.getdrinkcount(sex=sex, group='P')
        for count in counts:
            piedataset[count[0]][sex_choice.index(sex)][2] = count[1]
        counts = analyse.getdiabetescount(sex=sex, group='P')
        for count in counts:
            piedataset[count[0]][sex_choice.index(sex)][3] = count[1]
        counts=analyse.gethypertensioncount(sex=sex,group='P')
        for count in counts:
            piedataset[count[0]][sex_choice.index(sex)][4] = count[1]
        counts=analyse.gethyperlipemcount(sex=sex,group='P')
        for count in counts:
            piedataset[count[0]][sex_choice.index(sex)][5] = count[1]
    data = analyse.getusercount(sex=None, group='P')
    if data:
        dataset = analyse.convertdict(data)
        valmax = max([x[1] for x in data])
    return render(request, 'healthmanage/analye.html', locals())


@login_required
def password_change(request):
    user = request.user
#    userinfo=models.UserInfo.objects.get(user=user)
#    avatar = userinfo.photo
    return render(request, 'healthmanage/password_change_form.html',locals())
'''

@login_required   
def UserInfoView(request):
    user=request.user
    if request.method == "POST":
        form = forms.UserInfoModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)    
            post.save()
            return HttpResponse("数据提交成功！！")
    else:
        form = forms.UserInfoModelForm()
        return render(request, "healthmanage/userinfo_form.html", locals())


# API Views

from rest_framework import viewsets

class UserInfoViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代ArticleList和ArticleDetail两个视图
    queryset = UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    
    # 自行添加，将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET', 'POST'])
def userinfo_list(request, format=None):
    """
    List all UserInfo, or create a new UserInfo.
    """
    if request.method == 'GET':
        userinfos = UserInfo.objects.all()
        serializer = serializers.UserInfoSerializer(userinfos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer =  serializers.UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            # Very important. Associate request.user with user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def userinfo_detail(request, pk, format=None):
    """
    Retrieve，update or delete an userinfo instance。"""
    try:
        userinfo = UserInfo.objects.get(pk=pk)
    except UserInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.UserInfoSerializer(userinfo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.UserInfoSerializer(userinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        userinfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''