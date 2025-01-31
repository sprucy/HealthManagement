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
from django.conf import settings

from django.utils.translation import gettext as _


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
    assess=[]
    risks=[]
    intervents=[]
    val=''
    if userdata.getsmoke():
        if settings.LANGUAGE_CODE == 'en':
            val='Smoking' 
        else:
            val='吸烟'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))  
    if userdata.getdrink():
        if settings.LANGUAGE_CODE == 'en':
            val='Drinking'
        else:
            val='饮酒'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))   
    if userdata.getdiabetes():
        if settings.LANGUAGE_CODE == 'en':        
            val='Diabetes'
        else:
            val='糖尿病'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))    
    #体重
    bodyresult = userdata.getbodyinfoavg(avgnum)
    if assessresult:
        bmiresult = myhealth.bmiassess(bodyresult[3])
        assessresult.append(bmiresult)
        if settings.LANGUAGE_CODE == 'en':
            indicatorname = 'Under weight'
            indicatorlist = ['Over weight','Grade I obesity','Grade II obesity','BMI evaluation','Grade III obesity']
        else:
            indicatorname = '体重偏瘦'
            indicatorlist = ['体重偏胖','I度肥胖','II度肥胖','BMI评估','III度肥胖']
        if (bmiresult == indicatorname):
            if settings.LANGUAGE_CODE == 'en':
                val='Underweight'
            else:
                val='体重消瘦'

            risks.extend(myhealth.getrisks(val))
            intervents.extend(myhealth.getintervents(val))
        elif (bmiresult in indicatorlist):
            if settings.LANGUAGE_CODE == 'en':
                val = 'Obesity'
            else:
                val='体重肥胖'
            risks.extend(myhealth.getrisks(val))
            intervents.extend(myhealth.getintervents(val))
    #血压
    bloodpressureresult = userdata.getbloodpressureavg(avgnum)
    if assessresult:
        bpresult = myhealth.bloodppressureassess(bloodpressureresult)

        if bpresult[0] == _('Systolic blood pressure is high') or bpresult[1] == _('Diastolic blood pressure is high'):
            val = _('Hypertension') 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == _('Systolic blood pressure is low') or bpresult[1] == _('Diastolic blood pressure is low'):
            val = _('Hypotension') 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val)) 
    #血脂
    bcholesterinresult = userdata.getbcholesterinavg(avgnum)
    if assessresult:
        bpresult = myhealth.bcholesterinassess(bcholesterinresult)
        if bpresult[0] == _('Total cholesterol is high'):
            val = _('Hyperlipidemia') 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == _('Total cholesterol is low'):
            val = _('Hypolipidemia') 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
    if not val:
        risks =[[_('You have good daily habits and physical condition, which is the foundation of good health!')]]
        intervents=[[_('It is recommended to maintain good daily habits, control your diet, reduce salt, sugar, and oil, and at the same time strengthen physical exercise!')]]

    if assessresult:  
        assess.append(_('age')+': '+str(age)+','+_('Your 10-year absolute risk of developing ischemic cardiovascular disease (ICVD) was assessed as')+' '+str(assessresult[0])+','
                    +_('The minimum absolute risk of ischemic cardiovascular disease (ICVD) in the same age and gender was')+' '+str(assessresult[2])+','
                    +_('The 10-year average absolute risk of ischemic cardiovascular disease (ICVD) in the same age and sex is')+' '+str(assessresult[1])+',')
        if assessresult[0] > assessresult[1]:
            assess.append(_('Your evaluation result is')+' '+f'{assessresult[0]/assessresult[1]:.2f}'+_('times')+','+_('It is necessary to strengthen control to prevent the occurrence of ischemic cardiovascular disease (ICVD).'))
        else: 
            assess.append(_('Your risk of ischemic cardiovascular disease (ICVD) is lower.'))

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
        if settings.LANGUAGE_CODE == 'en':
            indicatorname = 'Under weight'
            indicatorlist = ['Over weight','Grade I obesity','Grade II obesity','BMI evaluation','Grade III obesity']
        else:
            indicatorname = '体重偏瘦'
            indicatorlist = ['体重偏胖','I度肥胖','II度肥胖','BMI评估','III度肥胖']

        if (bmiresult == indicatorname):
            if settings.LANGUAGE_CODE == 'en':
                val='Underweight'
            else:
                val='体重消瘦'
            risks.extend(myhealth.getrisks(val))
            intervents.extend(myhealth.getintervents(val))
        elif (bmiresult in indicatorlist):
            if settings.LANGUAGE_CODE == 'en':
                val = 'Obesity'
            else:
                val='体重肥胖'
            risks.extend(myhealth.getrisks(val))
            intervents.extend(myhealth.getintervents(val))
        else:
            risks.extend([[_('Your weight is very normal!')],])
            intervents.extend([[_('It is recommended to maintain and strengthen physical exercise at the same time.')]])
        normalweight = myhealth.getnormalweight(assessresult[0])
        normalwaist = myhealth.getnormalwaist(sex, assessresult[0])

        assess =[_('Your')+' '+_('BMI')+': '+str(assessresult[3])+','
                +_('height')+': '+str(assessresult[0])+'cm,'
                +_('weight')+': '+str(assessresult[1])+'kg,'
                +_('belong to')+' '+str(assessresult[4])+','
                +_('Normal weight for the same height')+':' 
                + str(normalweight[0])+'Kg-'+str(normalweight[1])+'Kg,'
                +_('waistline')+': '+str(assessresult[2])+'cm,'
                +_('Normal waistline for the same height')+':'
                +str(normalwaist[0])+'cm-'+str(normalwaist[1])+'cm.'] 

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
    assess=[]
    risks=[]
    intervents=[]
    val=''
    if userdata.getsmoke():
        if settings.LANGUAGE_CODE == 'en':
            val='Smoking' 
        else:
            val='吸烟'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))  
    if userdata.getdrink():
        if settings.LANGUAGE_CODE == 'en':
            val='Drinking'
        else:
            val='饮酒'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))   
    if userdata.getdiabetes():
        if settings.LANGUAGE_CODE == 'en':        
            val='Diabetes'
        else:
            val='糖尿病'
        risks.extend(myhealth.getrisks(val))  
        intervents.extend(myhealth.getintervents(val))    
    if not val:
        risks =[[_("You don't have the habit of smoking or drinking alcohol on a daily basis, nor do you have a history of diabetes. Having good daily habits is the foundation of good health!")]]
        intervents=[[_('It is recommended to maintain good daily habits, control your diet, reduce salt, sugar, and oil, and at the same time strengthen physical exercise!')]]

    if smokeyear == 0:
        assess.append(_('You have no habit of smoking'))
    else:
        assess.append(_('You have the habit of smoking')+','+_('you have')+' '+str(smokeyear)+_('years')+' '+_("smoking history"))
    if drinkyear == 0:
        assess.append(_('You have no habit of drinking alcohol'))
    else:
        assess.append(_('You have the habit of drinking')+','+_('you have')+' '+str(drinkyear)+_('years')+' '+_("drinking history"))

    if drinkyear == 0:
        assess.append(_('You have no history of diabetes'))
    else:
        assess.append(_('You have diabetes')+','+_('you have')+' '+str(diabetesyear)+_('years')+' '+_("history of diabetes"))


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
        assess=[]
        risks=[]
        intervents=[]
        val=''
        if bpresult[0] == _('Systolic blood pressure is high') or bpresult[1] == _('Diastolic blood pressure is high'):
            val = _('Hypertension') 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == _('Systolic blood pressure is low') or bpresult[1] == _('Diastolic blood pressure is low'):
            val = _('Hypotension')  
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val)) 
        else:
            risks.extend([[_('Congratulations, your blood pressure is normal, and having good daily habits is the foundation of good health!')]])
            intervents.extend([[_('It is recommended to maintain good daily habits, control diet, reduce salt, sugar and oil, and strengthen physical exercise.')]])

        risks.extend(myhealth.getrisks(bpresult[2]))  
        intervents.extend(myhealth.getintervents(bpresult[2])) 

        assess.append(_('Your recent average Systolic blood pressure')+f': {assessresult[0]:.2f}mmol/L,'+_('Normal Systolic blood pressure range')+f': {normaldbp[0]:.2f}-{normaldbp[1]:.2f}mmol/L,'+_('Your')+f' {bpresult[0]};')
        assess.append(_('Your recent average Diastolic blood pressure')+f': {assessresult[1]:.2f}mmol/L,'+_('Normal Diastolic blood pressure range')+f': {normalsbp[0]:.2f}-{normalsbp[1]:.2f}mmol/L,'+_('Your')+f' {bpresult[1]};')

        if val:
            assess.append(_('If this blood pressure value is measured in a quiet state and the measurement method is correct, according to the World Health Organization, you can be diagnosed with')+f' {val};') 
        assess.append(_('Your recent average Heart rate')+f': {assessresult[2]:.2f}bpm,'+_('Normal Heart rate range')+f': {normalhr[0]:.2f}-{normalhr[1]:.2f}bpm,'+_('Your')+f' {bpresult[2]};')

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
        assess = []
        risks=[]
        intervents=[]
        val=''
        if bpresult[0] == _('Total cholesterol is high'):
            val = _('Hyperlipidemia') 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        elif bpresult[0] == _('Total cholesterol is low'):
            val = _('Hypolipidemia') 
            risks.extend(myhealth.getrisks(val))  
            intervents.extend(myhealth.getintervents(val))   
        else:
            riskstr=''
            if bpresult[1] == _('Low density lipoprotein is low'):
                riskstr += _('Your ')+bpresult[1]+','+_('Pay attention to strengthening the intake of low-density lipoprotein.')
            if bpresult[2] == _('High density lipoprotein is low'):
                riskstr += _('Your ')+bpresult[2]+','+_('Pay attention to strengthening the intake of high-density lipoprotein.')
            if bpresult[3] == _('Triglycerides is low'):
                riskstr += _('Your ')+bpresult[3]+','+_('Pay attention to strengthening the intake of  triglycerides.')
            if bpresult[1] == _('Low density lipoprotein is high'):
                riskstr += _('Your ')+bpresult[1]+','+_('Pay attention to control the intake of low-density lipoprotein')
            if bpresult[2] == _('High density lipoprotein is high'):
                riskstr += _('Your ')+bpresult[2]+','+_('Pay attention to control the intake of high-density lipoprotein')
            if bpresult[3] == _('Triglycerides is high'):
                riskstr += _('Your ')+bpresult[3]+','+_('Be careful to control your intake of triglycerides')
            riskstr += _('Having good daily habits is the foundation of good health!')
            risks.extend([[riskstr]])    
            intervents.extend([[_('It is recommended to maintain good living habits, control diet, and strengthen physical exercise!')]])

        assess.append(_('Your recent average Low density lipoprotein')+f': {assessresult[1]:.2f}mmol/L,'+_('Normal LDL range')+f': {normalldl[0]:.2f}-{normalldl[1]:.2f}mmol/L,'+_('Your')+f' {bpresult[1]};')
        assess.append(_('Your recent average High density lipoprotein')+f': {assessresult[2]:.2f}mmol/L,'+_('Normal HDL range')+f': {normalhdl[0]:.2f}-{normalhdl[1]:.2f}mmol/L,'+_('Your')+f' {bpresult[2]};')
        assess.append(_('Your recent average Triglycerides')+f': {assessresult[3]:.2f}mmol/L,'+_('Normal Triglycerides range')+f': {normaltg[0]:.2f}-{normaltg[1]:.2f}mmol/L,'+_('Your')+f' {bpresult[3]};')

        if val:
            assess.append(_('If you have a physical examination as required, based on your total cholesterol, it can be diagnosed as')+f' {val},'+_('It is recommended to seek medical review.')) 


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
    if settings.LANGUAGE_CODE == 'en':
        provinces=['Beijing', 'Guangdong', 'Shanghai', 'Tianjin', 'Chongqing', 'Liaoning', 'Jiangsu', 'Hubei', 'Sichuan', 'Shaanxi', 
                'Hebei', 'Shanxi', 'Henan', 'Jilin', 'Heilongjiang', 'Inner Mongolia', 'Shandong', 'Anhui', 'Zhejiang', 'Fujian', 
                'Hunan', 'Guangxi', 'Jiangxi', 'Guizhou', 'Yunnan', 'Tibet', 'Hainan', 'Gansu', 'Ningxia', 'Qinghai', 'Xinjiang', 
                'Hong Kong', 'Macau', 'Taiwan']
    else:
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