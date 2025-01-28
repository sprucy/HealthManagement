from django.shortcuts import render
from django.contrib.auth.models import User

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
        val = '吸烟'
        risks.extend(myhealth.getrisks(val))
        intervents.extend(myhealth.getintervents(val))

    if userdata.getdrink():
        val = '饮酒'
        risks.extend(myhealth.getrisks(val))
        intervents.extend(myhealth.getintervents(val))

    if userdata.getdiabetes():
        val = '糖尿病'
        risks.extend(myhealth.getrisks(val))
        intervents.extend(myhealth.getintervents(val))

    if not val:
        risks = [['您日常没有吸烟和饮酒的习惯，也无糖尿病史，拥有良好的日常习惯是身体健康的基础！']]
        intervents = [['建议保持良好的日常习惯，控制饮食，少盐少糖少油，同时加强体育锻炼!']]


    if smokeyear == 0:
        assess.append("您日常无吸烟的习惯;")
    else:
        assess.append(f"您有吸烟的习惯,已有{smokeyear}年的吸烟史;")
    if drinkyear == 0:
        assess.append("您日常无饮酒的习惯;")
    else:
        assess.append(f"您有饮酒的习惯，已有{drinkyear}年的饮酒史;")
    if drinkyear == 0:
        assess.append("您无糖尿病史;")
    else:
        assess.append(f"您患有糖尿病，已有{diabetesyear}年的糖尿病史;")


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
        assess = f"您的体质指数{assessresult[3]},身高为{assessresult[0]}cm,体重为{assessresult[1]}kg,属于{assessresult[4]},相同身高的正常体重为{normalweight[0]}Kg-{normalweight[1]}Kg之间,腰围为{assessresult[2]}cm,相同身高的{'男性' if sex=='M' else '女性'}的正常腰围:{normalwaist[0]}cm-{normalwaist[1]}cm"

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

        assess.append(f'您的近{avgnum}次平均收缩压为{assessresult[0]}mmol/L,正常收缩压范围为{normaldbp[0]}-{normaldbp[1]}mmol/L,您的{bpresult[0]};您的近{avgnum}次平均舒张压为{assessresult[1]}mmol/L,正常舒张压范围为{normalsbp[0]}-{normalsbp[1]}mmol/L,您的{bpresult[1]};')
        if val:
            assess.append(f'此血压值如果在安静状态测量,且测量方法正确,根据世界卫生组织规定你可确诊为{val};') 
        assess.append(f'您的近{avgnum}次平均心率为{assessresult[2]}次/分钟,正常心率范围为{normalhr[0]}-{normalhr[1]}次/分钟,您{bpresult[2]};')


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

        assess.append(f'您的近{avgnum}次平均低密度脂蛋白为{assessresult[1]}mmol/L,正常低密度脂蛋白范围为{normalldl[0]}-{normalldl[1]}mmol/L,您的{bpresult[1]};')
        assess.append(f'您的近{avgnum}次平均低密度脂蛋白为{assessresult[2]}mmol/L,正常高密度脂蛋白范围为{normalhdl[0]}-{normalhdl[1]}mmol/L,您的{bpresult[2]};')
        assess.append(f'您的近{avgnum}次平均甘油三酯为{assessresult[3]}mmol/L,正常甘油三酯范围为{normaltg[0]}-{normaltg[1]}mmol/L,您的{bpresult[3]};')
        if val:
            assess.append(f'如果您按要求进行体检，根据您体检的总胆固醇，可确诊为{val},建议就医复查;') 

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
    if assessresult:  
        assess.append(f'您的年龄为{age}岁，经评估您缺血性心血管病(ICVD)十年发病绝对危险度为{assessresult[0]},'
                    +f'而经统计同龄同性别缺血性心血管病(ICVD)十年发病最小绝对危险度为{assessresult[2]},'
                    +f'您的评估结果是其{(assessresult[0]/assessresult[2]):.2f}倍;同龄同性别缺血性心血管病(ICVD)'
                    +f'十年发病平均绝对危险度为{assessresult[1]},')
        if assessresult[0] > assessresult[1]:
            assess.append(f'您的评估结果是其{assessresult[0]/assessresult[1]:.2f}倍;需要加强控制,防止缺血性心血管病(ICVD)的发生。')
        else: 
            assess.append(f'你缺血性心血管病(ICVD)的发生风险较低。')


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

