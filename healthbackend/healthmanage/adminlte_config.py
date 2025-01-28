# myserver/utils/adminlte_config.py
from django.conf import settings
from django.contrib.auth.models import User,Group
from adminlteui.core import AdminlteConfig,MenuItem

class HealthAdminlteConfig(AdminlteConfig):
    # 是否显示头像，默认为False
    show_avatar = True
    # 头像对应的url或者用户头像字段，默认为None，将渲染为adminlteui/static/admin/dist/img/default.jpg
    #avatar_field = request.user.head_avatar'
    # 用户名显示，默认为None，将渲染为request.user.username
    #username_field = request.user.username
    # 站点logo，默认为None，将渲染为adminlteui/static/admin/dist/img/default-log.svg
    site_logo = settings.MEDIA_URL + '/health-logo.png'
    # 站点主题，默认为None，将渲染为blue
    #skin = 'red'
    # 侧边栏布局，默认为fixed，可选：['boxed', 'fixed']
    #sidebar_layout = 'fixed'
    # 搜索框是否显示搜索框，默认为True
    #search_form = True 
    # 版权，默认为None，将渲染为django-adminlte-ui版本号
    copyright = 'Copyright © 2021-2024'
    #copyright = 'Copyright © 2021-2022 <a href="URL_ADDRESS    #copyright = 'Copyright © 2021-2022 <a href="https://github.com/huanglianghua/django-adminlte-ui">django-ad
    #copyright = 'Copyright © 2021-2022 <a href="URL_ADDRESS.com/huanglianghua/django-adminlte-ui">django-adminlte-ui</a>'
    # 欢迎标志（登录页），默认为None，将渲染为芝麻开门
    welcome_sign = 'Welcome for Health Manager!'

    group = Group.objects.get(name='健康管理')
    grouppermissions=[perm.content_type.app_label+'.'+perm.codename for perm in group.permissions.all()]
    main_menu = [
            MenuItem(label='healthmanage', name='Health Info', child=[
            MenuItem(label='healthmanage.UserInfo',name='User Info',  menu_type='model'),
            MenuItem(label='healthmanage.BodyInfo',name='Body Info', menu_type='model'), 
            MenuItem(label='healthmanage.SmokeDiabetesInfo', name='Smoke_Diabetes Info', menu_type='model'),
            MenuItem(label='healthmanage.BloodPressure',name='BloodPressure Info', menu_type='model'),                       
            MenuItem(label='healthmanage.Bcholesterin',name='Bcholesterin Info', menu_type='model'),  
        ]),
        MenuItem(label='healthmanage', name='Health Standard', child=[
            MenuItem(label='healthmanage.BMIScale',name='BMI Scale', menu_type='model'),
            MenuItem(label='healthmanage.Indicator',name='Health Indicator', menu_type='model'),
            MenuItem(label='healthmanage.RiskAnalyse',name='Risk Analysis', menu_type='model'),  
            MenuItem(label='healthmanage.HealthIntervent',name='Risk Intervent', menu_type='model'), 
            MenuItem(label='healthmanage.SingleAssess', name='Single Indicator',menu_type='model'), 
            MenuItem(label='healthmanage.SmokeScale', name='Smoke Scale', menu_type='model'),
            MenuItem(label='healthmanage.AgeScale', name='Age Scale', menu_type='model'),
            MenuItem(label='healthmanage.WeightScale',name='Weight Scale', menu_type='model'), 
            MenuItem(label='healthmanage.DiabetesScale',name='Diabetes Scale', menu_type='model'), 
            MenuItem(label='healthmanage.BloodPressureScale',name='BloodPressure Scale', menu_type='model'),
            MenuItem(label='healthmanage.TCScale',name='Bcholesterin Scale', menu_type='model'),  
            MenuItem(label='healthmanage.CommonRiskScale', name='CommonRisk Scale', menu_type='model'),  
            MenuItem(label='healthmanage.RiskEvaluatScale', name='RiskEvaluate Scale',menu_type='model'),                        
        ]),  
        MenuItem(label='healthmanage', name='Health Assessment', child=[
            MenuItem(label='', name='Daily Habits Assessment',url='/healthmanage/habitassess/', menu_type='link'), 
            MenuItem(label='', name='BMI Weight Assessment',url='/healthmanage/weightassess/', menu_type='link'), 
            MenuItem(label='', name='Blood Pressure Assessment',url='/healthmanage/bpassess/', menu_type='link'), 
            MenuItem(label='', name='Bcholesterin Assessment',url='/healthmanage/bsassess/', menu_type='link'), 
            MenuItem(label='', name='ICVD Risk Assessment',url='/healthmanage/icvdrisk/', menu_type='link'), 
        ]),              
        MenuItem(label='healthmanage', name='Health Analysis', child=[
            MenuItem(label='', name='General Analysis',url='/healthmanage/analye/', menu_type='link', permissions=grouppermissions), 
            MenuItem(label='', name='Smokers Distribution Analysis',url='/healthmanage/smokeanalye/', menu_type='link', permissions=grouppermissions), 
            MenuItem(label='', name='Drinkers Distribution Analysis',url='/healthmanage/drinkanalye/', menu_type='link', permissions=grouppermissions), 
            MenuItem(label='', name='Diabetes Distribution Analysis',url='/healthmanage/diabetesanalye/', menu_type='link', permissions=grouppermissions), 
            MenuItem(label='', name='Obese Distribution Analysis',url='/healthmanage/fatanalye/', menu_type='link', permissions=grouppermissions), 
            MenuItem(label='', name='Hypertensive Distribution Analysis',url='/healthmanage/hypertensionanalye/', menu_type='link', permissions=grouppermissions), 
            MenuItem(label='', name='hyperlipidemia Distribution Analysis',url='/healthmanage/hyperlipemanalye/', menu_type='link', permissions=grouppermissions), 

        ]), 

        MenuItem(label='auth', name='Certi & Auth', icon='fa-users', child=[
            MenuItem(label='auth.User', name='User', menu_type='model'),
            MenuItem(label='auth.Group', name='Group', menu_type='model'),
        ]),
    ]


