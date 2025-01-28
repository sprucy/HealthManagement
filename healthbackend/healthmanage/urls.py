from django.urls import path



from . import views


app_name = 'healthmanage'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'), 
    path('login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change, name='password_change'),
    path('icvdrisk/', views.icvdrisk, name='icvdrisk'), 
    path('weightassess/', views.weightassess, name='weightassess'), 
    path('habitassess/', views.habitassess, name='habitassess'), 
    path('bpassess/', views.bloodpressureassess, name='bpassess'),
    path('bsassess/', views.bcholesterinassess, name='bsassess'),     
    path('smokeanalye/', views.smokeanalye, name='smokeanalye'),
    path('drinkanalye/', views.drinkanalye, name='drinkanalye'),
    path('fatanalye/', views.fatanalye, name='fatanalye'),
    path('diabetesanalye/', views.diabetesanalye, name='diabetesanalye'),
    path('hyperlipemanalye/', views.hyperlipemanalye, name='hyperlipemanalye'),
    path('hypertensionanalye/', views.hypertensionanalye, name='hypertensionanalye'),
    path('analye/', views.analye, name='analye'),
]


