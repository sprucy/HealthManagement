from django.urls import re_path,include
from rest_framework.routers import DefaultRouter


from .views import *



app_name = 'api'
# API
urlpatterns = [
    #re_path('', include(router.urls)),
    re_path(r'^habitassess/', habitassess_api, name='habitassess'),
    re_path(r'^bmiassess/', bmiassess_api, name='bmiassess'),
    re_path(r'^bloodpressureassess/', bloodpressureassess_api, name='bloodpressureassess'),
    re_path(r'^bcholesterinassess/', bcholesterinassess_api, name='bcholesterinassess'),
    re_path(r'^icvdassess/', icvdassess_api, name='icvdassess'),
    
]

router = DefaultRouter()
router.register(r'users', viewset=UserViewSet, basename='users')
router.register(r'userinfos', viewset=UserInfoViewSet, basename='userinfos')
router.register(r'bodyinfos', viewset=BodyInfoViewSet, basename='bodyinfos')
router.register(r'smokediabetesinfos', viewset=SmokeDiabetesInfoViewSet, basename='smokediabetesinfos')
router.register(r'bloodpressures', viewset=BloodPressureViewSet, basename='bloodpressures')
router.register(r'bcholesterins', viewset=BcholesterinViewSet, basename='bcholesterins')

router.register(r'bmiscales', viewset=BMIScaleViewSet, basename='bmiscales') 
router.register(r'indicators', viewset=IndicatorViewSet, basename='indicators')      
router.register(r'riskanalyses', viewset=RiskAnalyseViewSet, basename='riskanalyses') 
router.register(r'healthintervents', viewset=HealthInterventViewSet, basename='healthintervents')
router.register(r'singleassesss', viewset=SingleAssessViewSet, basename='singleassesss')  
router.register(r'smokescales', viewset=SmokeScaleViewSet, basename='smokescales')
router.register(r'agescales', viewset=AgeScaleViewSet, basename='agescales')       
router.register(r'weightscales', viewset=WeightScaleViewSet, basename='weightscales')      
router.register(r'diabetesscales', viewset=DiabetesScaleViewSet, basename='diabetesscales')
router.register(r'bloodpressurescales', viewset=BloodPressureScaleViewSet, basename='bloodpressurescales')      
router.register(r'tcscales', viewset=TCScaleViewSet, basename='tcscales')   
router.register(r'commonriskscales', viewset=CommonRiskScaleViewSet, basename='commonriskscales')
router.register(r'riskevaluatscales', viewset=RiskEvaluatScaleViewSet, basename='riskevaluatscales') 

router.register(r'groups', viewset=GroupViewSet, basename='groups')
router.register(r'permissions', viewset=PermissionViewSet, basename='permissions')

urlpatterns += router.urls  # 追加路由
