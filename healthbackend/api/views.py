from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework import viewsets
from rest_framework import status
from rest_framework import authentication,permissions
from rest_framework import response, decorators
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import render

from healthmanage.models import *
from .serializers import *
from .permissions import IsOwner

from healthmanage.risks import *

succeed_response_schema = openapi.Response(
    description='请求成功',
    schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='刷新token'),
        'access': openapi.Schema(type=openapi.TYPE_STRING, description='访问token'),
    })
)
fail_response_schema = openapi.Response(
    description='请求失败',
    schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'errors': openapi.Schema(type=openapi.TYPE_STRING, description='错误信息'),
    })
)
# 用户登录
'''
@swagger_auto_schema(method='POST',  
                     operation_summary='用户登录', 
                     operation_description='用户登录,填写用户名密码',
                     responses={201: succeed_response_schema,400: fail_response_schema},
                    )
'''
class MyTokenObtainPair(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

# 用户注册函数视图文档自动生成
request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
        'password_confirm': openapi.Schema(type=openapi.TYPE_STRING, description='密码确认'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),        
    },
    required=['username','password','password_confirm','email']
)

@swagger_auto_schema(method='POST',  
                     operation_summary='用户注册', 
                     operation_description='用户注册,填写注册信息,返回400错误',
                     request_body=request_schema,
                     responses={201: succeed_response_schema,400: fail_response_schema}
                    )
# 用户注册函数视图定义
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)        
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_201_CREATED)

# API视图集

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def habitassess_api(request):
    user = request.user
    userdata = UserData(user)
    sex = userdata.getsex()
    age = userdata.getage()
    smokeyear = userdata.getsmokeyears()
    drinkyear = userdata.getdrinkyears()
    diabetesyear = userdata.getdiabetesyears()
    myhealth = HealthRiskAssess()
    assess=[]
    risks = []
    intervents = []
    val = ''


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



    context = {
        'id': user.id,
        'username': user.username,
        'name': user.last_name+' '+user.first_name,
        'sex': sex,
        'age': age,
        'smokeyear': smokeyear,
        'drinkyear': drinkyear,
        'diabetesyear': diabetesyear,
        'assess': assess,
        'risks': risks,
        'intervents': intervents,
    }

    # 将单个对象包装成一个数组，并返回包含 data 的对象
    response_data = {
        "count": 1,
        "next": "null",
        "previous": "null",
        "results": [context,],
    }

    return response.Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bmiassess_api(request):
    user = request.user
    #数据的天数
    num = 30
    #平均值的天数
    avgnum=7
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
        assess =(_('Your')+' '+_('BMI')+': '+str(assessresult[3])+','
                +_('height')+': '+str(assessresult[0])+'cm,'
                +_('weight')+': '+str(assessresult[1])+'kg,'
                +_('belong to')+' '+str(assessresult[4])+','
                +_('Normal weight for the same height')+':' 
                + str(normalweight[0])+'Kg-'+str(normalweight[1])+'Kg,'
                +_('waistline')+': '+str(assessresult[2])+'cm,'
                +_('Normal waistline for the same height')+':'
                +str(normalwaist[0])+'cm-'+str(normalwaist[1])+'cm.') 

    context = {
        'id': user.id,
        'username': user.username,
        'name': user.last_name+' '+user.first_name,
        'sex': sex,
        'age': age,
        'dataset': bddataset,
        'assessresult': assessresult,
        'bmiresult': bmiresult if assessresult else None,
        'assess': assess if assessresult else None,
        'risks': risks if assessresult else None,
        'intervents': intervents if assessresult else None,
    }

    # 将单个对象包装成一个数组，并返回包含 data 的对象
    response_data = {
        "count": 1,
        "next": "null",
        "previous": "null",
        "results": [context,],
    }

    return response.Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bloodpressureassess_api(request):
    user = request.user
    #数据的天数
    num = 30
    #平均值的天数
    avgnum=7
    userdata = UserData(user)

    sex = userdata.getsex()
    age = userdata.getage()
    assessresult = userdata.getbloodpressureavg(avgnum)
    myhealth = HealthRiskAssess()
    if assessresult:
        bpdataset = list(zip(*(userdata.getbloodpressure(num))))
        bpdataset.insert(0, ['measuretime','dbp','sbp','hr'])
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


    context = {
        'id': user.id,
        'username': user.username,
        'name': user.last_name+' '+user.first_name,
        'sex': sex,
        'age': age,
        'dataset': bpdataset if assessresult else None,
        'assessresult': assessresult if assessresult else None,
        'assess': assess if assessresult else None,
        'risks': risks if assessresult else None,
        'intervents': intervents if assessresult else None,
    }

    # 将单个对象包装成一个数组，并返回包含 data 的对象
    response_data = {
        "count": 1,
        "next": "null",
        "previous": "null",
        "results": [context,],
    }

    return response.Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bcholesterinassess_api(request):
    user = request.user
    #数据的天数
    num = 30
    #平均值的天数
    avgnum=7
    userdata = UserData(user)

    sex = userdata.getsex()
    age = userdata.getage()
    assessresult = userdata.getbodyinfoavg(avgnum)
    myhealth = HealthRiskAssess()
    if assessresult:
        bsdataset = list(zip(*(userdata.getbcholesterin(num))))
        bsdataset.insert(0, ['measuretime','tc', 'ldl',  'hdl', 'tg'])
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

    context = {
        'id': user.id,
        'username': user.username,
        'name': user.last_name+' '+user.first_name,
        'sex': sex,
        'age': age,
        'dataset': bsdataset if assessresult else None,
        'assessresult': assessresult if assessresult else None,
        'assess': assess if assessresult else None,
        'risks': risks if assessresult else None,
        'intervents': intervents if assessresult else None,
    }

    # 将单个对象包装成一个数组，并返回包含 data 的对象
    response_data = {
        "count": 1,
        "next": "null",
        "previous": "null",
        "results": [context,],
    }

    return response.Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def icvdassess_api(request):
    user = request.user

    #平均值的天数
    avgnum=7
    userdata = UserData(user)

    sex = userdata.getsex()
    age = userdata.getage()

    myhealth = HealthRiskAssess()
    assessresult = myhealth.icvdassess(userdata)
    risks=[]
    intervents=[]
    val=''
    assess=[]
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


    context = {
        'id': user.id,
        'username': user.username,
        'name': user.last_name+' '+user.first_name,
        'sex': sex,
        'age': age,
        'assessresult': assessresult,
        'assess': assess if assessresult else None,
        'risks': risks if assessresult else None,
        'intervents': intervents if assessresult else None,
    }

    # 将单个对象包装成一个数组，并返回包含 data 的对象
    response_data = {
        "count": 1,
        "next": "null",
        "previous": "null",
        "results": [context,],
    }

    return response.Response(response_data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = UserSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #permissions.DjangoModelPermissions,)#IsOwner,)
    # 分页采用了rest_framework.pagination.LimitOffsetPagination，放在了setting里定义
    # 过滤和排序定义
    #filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter,)
    # 过滤字段，对应DjangoFilterBackend(Django-Filter)
    #filterset_fields = ['sex', 'birthday']
    # 过滤字段，对应filters.SearchFilter(rest_framework)
    #search_fields = ('title',)
    # 排序字段，对应filters.OrderingFilter(rest_framework)
    #ordering_fields = ('id')
    # 数据集定义，查看所有数据

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)

class UserInfoViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = UserInfoSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 分页采用了rest_framework.pagination.LimitOffsetPagination，放在了setting里定义
    # 过滤和排序定义
    #filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter,)
    # 过滤字段，对应DjangoFilterBackend(Django-Filter)
    #filterset_fields = ['sex', 'birthday']
    # 过滤字段，对应filters.SearchFilter(rest_framework)
    #search_fields = ('title',)
    # 排序字段，对应filters.OrderingFilter(rest_framework)
    #ordering_fields = ('id')
    # 数据集定义，用户只能看到自己的数据。
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return UserInfo.objects.all()
        else:
            return UserInfo.objects.filter(user=user)

class BodyInfoViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = BodyInfoSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)

    # 数据集定义，用户只能看到自己的数据。
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return BodyInfo.objects.all()
        else:
            return BodyInfo.objects.filter(user=user)

class SmokeDiabetesInfoViewSet(viewsets.ModelViewSet):
    serializer_class = SmokeDiabetesInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SmokeDiabetesInfo.objects.all()
        else:
            return SmokeDiabetesInfo.objects.filter(user=user)

class BloodPressureViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = BloodPressureSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，用户只能看到自己的数据。
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return BloodPressure.objects.all()
        else:
            return BloodPressure.objects.filter(user=user)
        
class BcholesterinViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = BcholesterinSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Bcholesterin.objects.all()
        else:
            return Bcholesterin.objects.filter(user=user)

class BMIScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = BMIScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = BMIScale.objects.all()
    
class IndicatorViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = IndicatorSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = Indicator.objects.all()

class RiskAnalyseViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = RiskAnalyseSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset =RiskAnalyse.objects.all()
    
class HealthInterventViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = HealthInterventSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset =HealthIntervent.objects.all()

class SingleAssessViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = SingleAssessSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = SingleAssess.objects.all()
    
class SmokeScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = SmokeScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = SmokeScale.objects.all()

class AgeScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = AgeScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = AgeScale.objects.all()
        
class WeightScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = WeightScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = WeightScale.objects.all()    
    
class DiabetesScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = DiabetesScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = DiabetesScale.objects.all()

class BloodPressureScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = BloodPressureScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = BloodPressureScale.objects.all()
       
class TCScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = TCScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = TCScale.objects.all()
       
class CommonRiskScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = CommonRiskScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = CommonRiskScale.objects.all()
    
class RiskEvaluatScaleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = RiskEvaluatScaleSerializer
    # 定义权限
    permission_classes = (permissions.IsAuthenticated,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = RiskEvaluatScale.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = GroupSerializer
    # 定义权限
    permission_classes = (permissions.IsAdminUser,) #DjangoModelPermissions,IsOwner,)
    #authentication_classes = [authentication.TokenAuthentication]
    # 数据集定义，查看所有数据
    queryset = Group.objects.all().order_by('id')

class PermissionViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代UserInfoList和UserInfoDetail两个视图
    serializer_class = PermissionSerializer
    # 定义权限
    permission_classes = (permissions.IsAdminUser,) #DjangoModelPermissions,IsOwner,)
    # 数据集定义，查看所有数据
    queryset = Permission.objects.all().order_by('id')


'''    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='健康管理').exists():
            return UserInfo.objects.all()
        elif user.is_authenticated:
            return UserInfo.objects.filter(user=user)    

    # 设置当前用户为对象的所有者
    def perform_create(self, serializer):
        serializer.save(userr=self.request.user)
'''
'''
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
    Retrieve,update or delete an userinfo instance。"""
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

