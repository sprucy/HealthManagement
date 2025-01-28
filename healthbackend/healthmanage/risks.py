from django.contrib.auth.models import User
from django.db.models import Avg,Q,Count,Min,Max
from django.db.models.functions import TruncYear,TruncMonth,TruncDay
import datetime
import time
import numpy as np
import logging 

from .models import *

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  

class AnalyseStatistics(object):
    def __init__(self):
        pass
    #将列表转换为echart地图使用的字典
    #参数：列表[[data[0],data[1]]]
    #返回值：字典[{'name':data[0],'value':data[1]}]
    def convertdict(self, data):
        title = ['name', 'value']
        dataset=[]
        for d in data:
            if d[0]:
                dataset.append(dict(zip(title, d)))
        return dataset
    #统计用户人数
    #参数: sex-按性别统计，None：全部，M：男性，F:女性
    #      group-分组，None：不分组，C:按城市分组，P：按省分组
    def getusercount(self,sex=None,group=None):
        if sex is None:
            #所有吸烟的用户
            if group == 'P':
                #按省分组统计吸烟用户数量
                num = User.objects.all().values('userinfo__province').annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计吸烟用户数量
                num = User.objects.all().values('userinfo__city').annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计吸烟用户总数
                num = User.objects.all().count()
        else:
            if group == 'P':
                #按省分组统计特定性别吸烟用户数量
                num  = User.objects.all().values('userinfo__province','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计特定性别吸烟用户数量
                num  = User.objects.all().values('userinfo__city','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计特定性别吸烟用户总数
                num = User.objects.all().values('userinfo__sex').filter(userinfo__sex=sex).count()
        return num
    #统计吸烟人数
    #参数: sex-按性别统计，None：全部，M：男性，F:女性
    #      group-分组，None：不分组，C:按城市分组，P：按省分组
    def getsmokecount(self,sex=None,group=None):
        user = SmokeDiabetesInfo.objects.filter(smoke=True).values_list('user')
        if sex is None:
            #所有吸烟的用户
            if group == 'P':
                #按省分组统计吸烟用户数量
                num = User.objects.filter(id__in=user).values('userinfo__province').annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计吸烟用户数量
                num = User.objects.filter(id__in=user).values('userinfo__city').annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计吸烟用户总数
                num = User.objects.filter(id__in=user).count()
        else:
            if group == 'P':
                #按省分组统计特定性别吸烟用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__province','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计特定性别吸烟用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__city','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计特定性别吸烟用户总数
                num = User.objects.filter(id__in=user).values('userinfo__sex').filter(userinfo__sex=sex).count()
        return num
    #统计饮酒人数
    #参数: sex-按性别统计，None：全部，M：男性，F:女性
    #      group-分组，None：不分组，C:按城市分组，P：按省分组
    def getdrinkcount(self,sex=None,group=None):
        user = SmokeDiabetesInfo.objects.filter(drink=True).values_list('user')
        if sex is None:
            #所有饮酒的用户
            if group == 'P':
                #按省分组统计饮酒用户数量
                num = User.objects.filter(id__in=user).values('userinfo__province').annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计饮酒用户数量
                num = User.objects.filter(id__in=user).values('userinfo__city').annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计饮酒用户总数
                num = User.objects.filter(id__in=user).count()
        else:
            if group == 'P':
                #按省分组统计特定性别饮酒用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__province','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计特定性别饮酒用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__city','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计特定性别饮酒用户总数
                num = User.objects.filter(id__in=user).values('userinfo__sex').filter(userinfo__sex=sex).count()
        return num
    #统计糖尿病人数
    #参数: sex-按性别统计，None：全部，M：男性，F:女性
    #      group-分组，None：不分组，C:按城市分组，P：按省分组
    def getdiabetescount(self,sex=None,group=None):
        user = SmokeDiabetesInfo.objects.filter(diabetes=True).values_list('user')
        if sex is None:
            #所有糖尿病的用户
            if group == 'P':
                #按省分组统计糖尿病用户数量
                num = User.objects.filter(id__in=user).values('userinfo__province').annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计糖尿病用户数量
                num = User.objects.filter(id__in=user).values('userinfo__city').annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计糖尿病用户总数
                num = User.objects.filter(id__in=user).count()
        else:
            if group == 'P':
                #按省分组统计特定性别糖尿病用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__province','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计特定性别糖尿病用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__city','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计特定性别糖尿病用户总数
                num = User.objects.filter(id__in=user).values('userinfo__sex').filter(userinfo__sex=sex).count()
        return num
    #统计高血压人数
    #参数: sex-按性别统计，None：全部，M：男性，F:女性
    #      group-分组，None：不分组，C:按城市分组，P：按省分组
    def getfatcount(self, sex=None, group=None):
        users = User.objects.all()
        user=[]
        for curuser in users:
            userdata = UserData(curuser)
            if userdata and userdata.getfat():
                user.append(userdata.getuserid())
        if sex is None:
            #所有高血压的用户
            if group == 'P':
                #按省分组统计高血压用户数量
                num = User.objects.filter(id__in=user).values('userinfo__province').annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计高血压用户数量
                num = User.objects.filter(id__in=user).values('userinfo__city').annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计高血压用户总数
                num = User.objects.filter(id__in=user).count()
        else:
            if group == 'P':
                #按省分组统计特定性别高血压用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__province','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计特定性别高血压用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__city','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计特定性别高血压用户总数
                num = User.objects.filter(id__in=user).values('userinfo__sex').filter(userinfo__sex=sex).count()
        return num
    #统计高血压人数
    #参数: sex-按性别统计，None：全部，M：男性，F:女性
    #      group-分组，None：不分组，C:按城市分组，P：按省分组
    def gethypertensioncount(self, sex=None, group=None):
        users = User.objects.all()
        user=[]
        for curuser in users:
            userdata = UserData(curuser)
            if userdata and userdata.gethypertension():
                user.append(userdata.getuserid())
        if sex is None:
            #所有高血压的用户
            if group == 'P':
                #按省分组统计高血压用户数量
                num = User.objects.filter(id__in=user).values('userinfo__province').annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计高血压用户数量
                num = User.objects.filter(id__in=user).values('userinfo__city').annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计高血压用户总数
                num = User.objects.filter(id__in=user).count()
        else:
            if group == 'P':
                #按省分组统计特定性别高血压用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__province','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计特定性别高血压用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__city','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计特定性别高血压用户总数
                num = User.objects.filter(id__in=user).values('userinfo__sex').filter(userinfo__sex=sex).count()
        return num
    #统计高脂血人数
    #参数: sex-按性别统计，None：全部，M：男性，F:女性
    #      group-分组，None：不分组，C:按城市分组，P：按省分组
    def gethyperlipemcount(self, sex=None, group=None):
        users = User.objects.all()
        user=[]
        for curuser in users:
            userdata = UserData(curuser)
            if userdata and userdata.gethyperlipem():
                user.append(userdata.getuserid())
        if sex is None:
            #所有高脂血的用户
            if group == 'P':
                #按省分组统计高脂血用户数量
                num = User.objects.filter(id__in=user).values('userinfo__province').annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计高脂血用户数量
                num = User.objects.filter(id__in=user).values('userinfo__city').annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计高脂血用户总数
                num = User.objects.filter(id__in=user).count()
        else:
            if group == 'P':
                #按省分组统计特定性别高脂血用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__province','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__province')).values_list('userinfo__province','num')
            elif group == 'C':
                #按市分组统计特定性别高脂血用户数量
                num  = User.objects.filter(id__in=user).values('userinfo__city','userinfo__sex').filter(userinfo__sex=sex).annotate(num=Count('userinfo__city')).values_list('userinfo__city','num')
            else:
                #统计特定性别高脂血用户总数
                num = User.objects.filter(id__in=user).values('userinfo__sex').filter(userinfo__sex=sex).count()
        return num
class UserData(object):
    def __init__(self,user):
        self.user=user
        self.userinfo = UserInfo.objects.filter(user=user).first()
        self.smokediabetes = SmokeDiabetesInfo.objects.filter(user=user).first()
        self.bodyinfo = BodyInfo.objects.filter(user=user).order_by('-measuretime')
        self.bloodpressure = BloodPressure.objects.filter(user=user).order_by('-measuretime')
        self.bcholesterin = Bcholesterin.objects.filter(user=user).order_by('-measuretime')
    # 获取用户
    # 返回值：用户-queryset类型
    def getuser(self):
        return self.user
    #获取用户id
    def getuserid(self):
        return self.user.pk
    #获取用户姓名
    def getusername(self):
        return self.user.lastname+self.user.firstname

    #获取当前用户性别,
    # 返回值：男性-'M'，女性-'F'，当无userinfo数据时，返回None
    def getsex(self):
        if self.userinfo:
            return self.userinfo.sex
        else:
            return None
    # 获取当前用户年龄
    # 返回值：年龄(int)，当无userinfo数据时，返回None
    def getage(self):
        if self.userinfo:
            return datetime.date.today().year - self.userinfo.birthday.year
        else:
            return None
    # 是否吸烟
    # 返回值；True/False，当无smokediabetes数据时，返回None
    def getsmoke(self):
        if self.smokediabetes:
            return self.smokediabetes.smoke
        else:
            return None
    # 吸烟年限
    # 返回值：无smokediabetes数据-None,不吸烟-0，吸烟-吸烟时间(年)
    def getsmokeyears(self):
        if self.smokediabetes:
            if self.smokediabetes.smoke:
                return datetime.date.today().year - self.smokediabetes.smokestart.year
            else:
                return 0
        else:
            return None        
    # 是否饮酒
    # 返回值；True/False，当无smokediabetes数据时，返回None
    def getdrink(self):
        if self.smokediabetes:
            return self.smokediabetes.drink
        else:
            return None
    # 返回饮酒年限
    # 返回值：无smokediabetes数据-None,不饮酒-0，饮酒-饮酒时间(年)
    def getdrinkyears(self):
        if self.smokediabetes:
            if self.smokediabetes.drink:
                return datetime.date.today().year - self.smokediabetes.drinkstart.year
            else:
                return 0
        else:
            return None
    # 返回是否糖尿病患者
    # 返回值；True/False，当无smokediabetes数据时，返回None
    def getdiabetes(self):
        if self.smokediabetes:        
            return self.smokediabetes.diabetes
        else:
            return None            
    # 返回糖尿病患病年限
    # 返回值：无smokediabetes数据-None,无糖尿病-0，糖尿病-糖尿病时间(年)
    def getdiabetesyears(self):
        if self.smokediabetes:
            if self.smokediabetes.diabetes:
                return datetime.date.today().year - self.smokediabetes.diabetesstart.year
            else:
                return 0
        else:
            return None
    # 获取最后num次的身高体重
    # 参数：num为统计次数
    # 返回值：二维列表[[统计时间],[身高],[体重],[腰围],[BMI]]
    def getbodyinfo(self, num):
        if self.bodyinfo:        
            #取当前用户最后num天的身高、体重、腰围的平均值（如果每天多次测量取平均值）
            #第一行按measuretime的年月日分组
            #第二行按上行的分组计算身高、体重、腰围的平均值，
            #第三行身高、体重、腰围平均值为列表，并利用切片取前最后num天的值 
            avglist = self.bodyinfo.annotate(days=TruncDay('measuretime')).values('days')\
                .annotate(heightavg=Avg('height'),weightavg=Avg('weight'),waistavg=Avg('waist'))\
                .values('days', 'heightavg', 'weightavg', 'waistavg')[:num]
            #求平均值,日期从前向后，反向迭代取出列表
            dataset=[[m.strftime('%Y-%m-%d') for m in reversed(avglist.values_list('days', flat=True))]]
            dataset.append([float(value) for value in reversed(avglist.values_list('height', flat=True))])
            dataset.append([float(value) for value in reversed(avglist.values_list('weight', flat=True))])
            dataset.append([float(value) for value in reversed(avglist.values_list('waist', flat=True))])
            dataset.append([round(w * 10000 / h / h, 2) for w, h in zip(dataset[2], dataset[1])])       
            return dataset
        else:
            return None        
    # 获取最后num次的血压
    # 参数：num为统计次数
    # 返回值：二维列表[[统计时间],[收缩压],[舒张压],[心率]]
    def getbloodpressure(self, num):
        if self.bloodpressure:        
            avglist = self.bloodpressure.annotate(days=TruncDay('measuretime')).values('days')\
                .annotate(DBPavg=Avg('DBP'),SBPavg=Avg('SBP'),HRavg=Avg('HR'))\
                .values_list('days', 'DBPavg', 'SBPavg', 'HRavg')[:num]
            dataset=[[m.strftime('%Y-%m-%d') for m in reversed(avglist.values_list('days', flat=True))]]
            dataset.append([float(value) for value in reversed(avglist.values_list('DBPavg', flat=True))])
            dataset.append([float(value) for value in reversed(avglist.values_list('SBPavg', flat=True))])
            dataset.append([float(value) for value in reversed(avglist.values_list('HRavg', flat=True))])     
            return dataset
        else:
            return None       
    # 获取最后num次的血脂
    # 参数：num为统计次数
    # 返回值：二维列表[[统计时间],[总胆固醇],[低密度],[高密度],[甘油三酯]]
    def getbcholesterin(self, num):
        if self.bcholesterin: 
            avglist = self.bcholesterin.annotate(days=TruncDay('measuretime')).values('days')\
                .annotate(TCavg=Avg('TC'),LDLavg=Avg('LDL'),HDLavg=Avg('HDL'),TGavg=Avg('TG'))\
                .values_list('days', 'TCavg', 'LDLavg',  'HDLavg', 'TGavg')[:num]

            dataset=[[m.strftime('%Y-%m-%d') for m in reversed(avglist.values_list('days', flat=True))]]
            dataset.append([float(value) for value in reversed(avglist.values_list('TCavg', flat=True))])
            dataset.append([float(value) for value in reversed(avglist.values_list('LDLavg', flat=True))])
            dataset.append([float(value) for value in reversed(avglist.values_list('HDLavg', flat=True))])     
            dataset.append([float(value) for value in reversed(avglist.values_list('TGavg', flat=True))])
            return dataset
        else:
            return None  

    # 获取最后num次的平均身高体重
    # 参数：num为统计次数
    # 返回值：一维列表[平均身高,平均体重,平均腰围,平均BMI]
    def getbodyinfoavg(self, num):
        if self.bodyinfo:        
            avglist = self.bodyinfo.annotate(days=TruncDay('measuretime')).values('days')\
                .annotate(heightavg=Avg('height'),weightavg=Avg('weight'),waistavg=Avg('waist'))\
                .values_list('heightavg', 'weightavg', 'waistavg')[:num]
            #求平均值
            avglist = np.array(avglist).mean(axis=0)
            height = round(float(avglist[0]), 2)          
            weight = round(float(avglist[1]), 2)
            waist = round(float(avglist[2]), 2)
            bmi=round(weight * 10000 / height / height, 2)
            return [height,weight,waist,bmi]
        else:
            return None        
    # 获取最后num次的平均血压
    # 参数：num为统计次数，
    # 返回值：一维列表[平均收缩压,平均舒张压,平均心率]
    def getbloodpressureavg(self, num):
        if self.bloodpressure:        
            avglist = self.bloodpressure.annotate(days=TruncDay('measuretime')).values('days')\
                .annotate(DBPavg=Avg('DBP'),SBPavg=Avg('SBP'),HRavg=Avg('HR'))\
                .values_list('DBPavg','SBPavg','HRavg')[:num]
            avglist = np.array(avglist).mean(axis=0)
            DBP = int(float(avglist[0]))          
            SBP = int(float(avglist[1]))
            HR = int(float(avglist[2]))
            return [DBP,SBP,HR]
        else:
            return None   
        
     # 获取最后num次的平均血脂
     # 参数：num为统计次数，
     # 返回值：一维列表[平均总胆固醇,平均低密度,平均高密度,平均甘油三酯]
    def getbcholesterinavg(self, num):
        if self.bcholesterin: 
            avglist = self.bcholesterin.annotate(days=TruncDay('measuretime')).values('days')\
                .annotate(TCavg=Avg('TC'),LDLavg=Avg('LDL'),HDLavg=Avg('HDL'),TGavg=Avg('TG'))\
                .values_list('TCavg','LDLavg','HDLavg','TGavg')[:num]
            avglist = np.array(avglist).mean(axis=0)
            TC = round(float(avglist[0]), 2)
            LDL = round(float(avglist[1]), 2)          
            HDL = round(float(avglist[2]), 2)
            TG = round(float(avglist[3]), 2)
            return [TC,LDL,HDL,TG]
        else:
            return None   
    #返回用户是否为肥胖
    def getfat(self):
        healthrisk = HealthRiskAssess()
        avg=self.getbodyinfoavg(3)
        if avg:
            result=healthrisk.bmiassess(avg[3])
            if (result in ['体重偏胖','I度肥胖','II度肥胖','III度肥胖']):
                return True
            else:
                return False
        else:
            return None
    #返回用户是否为高血压
    def gethypertension(self):
        healthrisk = HealthRiskAssess()
        avg=self.getbloodpressureavg(3)
        if avg:
            result=healthrisk.bloodppressureassess(avg)
            if result[0] == '收缩压较高' or result[1] == '舒张压较高':
                return True
            else:
                return False
        else:
            return None
    #返回用户是否为高脂血
    def gethyperlipem(self):
        healthrisk = HealthRiskAssess()
        avg=self.getbcholesterinavg(3)
        if avg:
            result = healthrisk.bcholesterinassess(avg)
            if result[0] == '总胆固醇较高':
                return True
            else:
                return False
        else:
            return None

#健康风险评估类 
class HealthRiskAssess(object):
    def __init__(self):
        #初始化bmi评估标准
        bmiscale = np.array(BMIScale.objects.all().values_list('bmi', 'wtype'))
        self.bmiscale=bmiscale[np.lexsort(bmiscale.T)].transpose()
        self.weighttypes={}
        indicator= Indicator.objects.filter(name='BMI评价').first()    
        for ind in Indicator.objects.filter(parent=indicator).values_list('id','name'):
            self.weighttypes[ind[0]]= ind[1]        
        #初始化单项评估标准
        self.singlescale = np.array(SingleAssess.objects.all().values_list('assesstype', 'assessname', 'minv', 'maxv'))

        #初始化icvd评估标准
        self.icvdscale = {}
        for sex in ('M','F'):
            agescale =  np.array(AgeScale.objects.filter(sex=sex).values_list('maxv','score'))
            weightscale = np.array(WeightScale.objects.filter(sex=sex).values_list('maxv','score'))
            bloodpPressurescale =  np.array(BloodPressureScale.objects.filter(sex=sex).values_list('maxv','score'))
            tcscale =  np.array(TCScale.objects.filter(sex=sex).values_list('maxv','score'))
            smokescale =  np.array(SmokeScale.objects.filter(sex=sex).values_list('smoke','score'))
            diabetesscale =  np.array(DiabetesScale.objects.filter(sex=sex).values_list('diabetes','score'))
            riskevaluatscale =  np.array(RiskEvaluatScale.objects.filter(sex=sex).values_list('score','risk'))
            commonriskscale =  np.array(CommonRiskScale.objects.filter(sex=sex).values_list('age','avgrisk','minrisk'))
            
            #对评价数组按最后一列排序，并进行转置为[[值],[得分]]形式
            agescale=agescale[np.lexsort(agescale.T)].transpose()
            weightscale=weightscale[np.lexsort(weightscale.T)].transpose()
            bloodpPressurescale=bloodpPressurescale[np.lexsort(bloodpPressurescale.T)].transpose()
            tcscale=tcscale[np.lexsort(tcscale.T)].transpose()    
            smokescale=smokescale[np.lexsort(smokescale.T)].transpose()
            diabetesscale=diabetesscale[np.lexsort(diabetesscale.T)].transpose()
            riskevaluatscale=riskevaluatscale[np.lexsort(riskevaluatscale.T)].transpose()
            commonriskscale=commonriskscale[np.lexsort(commonriskscale.T)].transpose()
            self.icvdscale[sex] = {'agescale': agescale,
                        'weightscale':weightscale,
                        'bloodppressurescale':bloodpPressurescale,
                        'tcscale':tcscale,
                        'smokescale':smokescale,
                        'diabetesscale':diabetesscale,
                        'riskevaluatscale':riskevaluatscale,
                        'commonriskscale': commonriskscale}
    #icvd数值标准评分判定函数
    # 参数：sex-性别，htype-所欲评估的类型,icvdscale字典的key值，val-所欲评估类型的值，
    # 返回结果：评估的得分，如无评估标准数据返回None
    def getvalscale(self, sex, htype, val):
        if sex in self.icvdscale:
            thescale = self.icvdscale[sex]
            if htype in thescale:                       
                return thescale[htype][1][np.searchsorted(thescale[htype][0], val, side='right')]
            else:
                return None
        else:
            return None
    #icvd布尔值标准评分判定函数
    # 参数：sex-性别，htype-所欲评估的类型,icvdscale字典的key值，val-所欲评估类型的值，
    # 返回结果：评估的得分，如无评估标准数据返回None
    def getboolscale(self, sex, htype, val):
        if sex in self.icvdscale:
            thescale = self.icvdscale[sex]
            if htype in thescale:               
                return thescale[htype][1][np.searchsorted(thescale[htype][0], val)]
            else:
                return None
        else:
            return None
    # 体重风险评估
    # 参数：bmival-bmi值，
    # 返回结果：体重评价结果，如体重偏瘦、体重肥胖等，如无评估标准数据返回None
    def bmiassess(self, bmival):
        if bmival:
            if self.bmiscale.size:
                return self.weighttypes[self.bmiscale[1][np.searchsorted(self.bmiscale[0], bmival, side='right')]]
        return None

    # 获取特定身高的标准体重范围
    # 参数：height-身高值
    # 返回结果：该身高的正常体重列表[最小正常体重,最大正常体重]
    def getnormalweight(self, height):
        if height:
            if self.bmiscale.size:
                val = height * height / 10000.0
                return [round(float(self.bmiscale[0][0]) * val, 2), round(float(self.bmiscale[0][1]) * val, 2)]
        return None
    # 获取特定性别和身高的标准腰围范围
    # 参数：sex-性别, height-身高值
    # 返回结果：同性别该身高的正常腰围列表[最小正常腰围,最大正常腰围]
    def getnormalwaist(self, sex, height):
        if sex=='M':
            val = 0.47
        else:
            val = 0.37
        return [round(height*val*0.95,2),round(height*val*1.05,2)]

    # 获取收缩压正常范围
    # 返回结果：收缩压正常范围列表[最大值,最小值]，如无评估标准数据返回None
    def getdbp(self):
        for assessname in self.singlescale:
            if assessname[1] == '收缩压':
                return [int(float(assessname[2])),int(float(assessname[3]))]
        return None

    # 获取舒张压正常范围
    # 返回结果：舒张压正常范围列表[最大值,最小值]，如无评估标准数据返回None
    def getsbp(self):
        for assessname in self.singlescale:
            if assessname[1] == '舒张压':
                return [int(float(assessname[2])),int(float(assessname[3]))]
        return None
    # 获取心率正常范围
    # 返回结果：心率正常范围列表[最大值,最小值]，如无评估标准数据返回None
    def gethr(self):
        for assessname in self.singlescale:
            if assessname[1] == '心率':
                return [int(float(assessname[2])),int(float(assessname[3]))]
        return None
    # 血压风险评估
    # 参数：pbval-血压值列表[收缩压, 舒张压，心率]
    # 返回结果： 血压评价结果列表，如无评估标准数据返回None
    def bloodppressureassess(self, val):
        dbp=self.getdbp()
        sbp=self.getsbp()
        hr=self.gethr()
        result = []
        if val and dbp and sbp and hr:
            if val[0]<dbp[0]:
                result.append('收缩压较低')
            elif val[0]>dbp[1]:
                result.append('收缩压较高')
            else:
                result.append('收缩压正常')
            if val[1]<sbp[0]:
                result.append('低舒张较低')
            elif val[1]>sbp[1]:
                result.append('高舒张压')
            else:
                result.append('舒张压正常')
            if val[2]<hr[0]:
                result.append('心动过缓')
            elif val[2]>hr[1]:
                result.append('心动过速')
            else:
                result.append('心率正常')
            return result
        return None

    # 获取总胆固醇正常范围
    # 返回结果：总胆固醇正常范围列表[最大值,最小值]，如无评估标准数据返回None
    def gettc(self):
        for assessname in self.singlescale:
            if assessname[1] == '总胆固醇':
                return [round(float(assessname[2]),2),round(float(assessname[3]),2)]
        return None
        
    # 获取低密度脂蛋白正常范围
    # 返回结果：低密度脂蛋白正常范围列表[最大值,最小值]，如无评估标准数据返回None
    def getldl(self):
        for assessname in self.singlescale:
            if assessname[1] == '低密度':
                return [round(float(assessname[2]),2),round(float(assessname[3]),2)]
        return None
        
    # 获取高密度脂蛋白正常范围
    # 返回结果：高密度脂蛋白正常范围列表[最大值,最小值]，如无评估标准数据返回None
    def gethdl(self):
        for assessname in self.singlescale:
            if assessname[1] == '高密度':
                return [round(float(assessname[2]),2),round(float(assessname[3]),2)]
        return None
        
    # 获取甘油三酯正常范围
    # 返回结果：甘油三酯正常范围列表[最大值,最小值]，如无评估标准数据返回None
    def gettg(self):
        for assessname in self.singlescale:
            if assessname[1] == '甘油三酯':
                return [round(float(assessname[2]),2),round(float(assessname[3]),2)]
        return None
        # 血压风险评估
    # 参数：pbval-血压值列表[收缩压, 舒张压，心率]
    # 返回结果： 血压评价结果列表，如无评估标准数据返回None
    def bcholesterinassess(self, val):
        tc=self.gettc()
        ldl=self.getldl()
        hdl = self.gethdl()
        tg=self.gettg()
        result = []
        if val and tc and ldl and hdl and tg:
            if val[0]<tc[0]:
                result.append('总胆固醇较低')
            elif val[0]>tc[1]:
                result.append('总胆固醇较高')
            else:
                result.append('总胆固醇正常')
            if val[1]<ldl[0]:
                result.append('低密度脂蛋白较低')
            elif val[1]>ldl[1]:
                result.append('低密度脂蛋白较高')
            else:
                result.append('低密度脂蛋白正常')
            if val[2]<hdl[0]:
                result.append('高密度脂蛋白较低')
            elif val[2]>hdl[1]:
                result.append('高密度脂蛋白较高')
            else:
                result.append('高密度脂蛋白正常')
            if val[3]<tg[0]:
                result.append('甘油三酯较低')
            elif val[3]>tg[1]:
                result.append('甘油三酯较高')
            else:
                result.append('甘油三酯正常')
            return result
        else:
            return None  
    # 返回当前得分的icvd十年发病风险百分比和同龄同性别icvd十年发病平均风险及最小风险
    # 参数：sex-性别, age-年龄, val-icvd评估得分
    # 返回结果：icvd十年发病风险百分比列表[评估人icvd十年发病风险百分比,同龄同性别icvd十年发病平均风险,同龄同性别icvd十年发病最小风险]
    def geticvd(self, sex, age, val):
        if sex in self.icvdscale:
            thescale = self.icvdscale[sex]
            print(np.searchsorted(thescale['riskevaluatscale'][0], val),len(thescale['riskevaluatscale'][0]))
            if 'riskevaluatscale' in thescale:       
                searchval = np.searchsorted(thescale['riskevaluatscale'][0], val)
                if searchval >= len(thescale['riskevaluatscale'][0]):
                    searchval = len(thescale['riskevaluatscale'][0])-1       
                myrisk = thescale['riskevaluatscale'][1][searchval]
                if 'commonriskscale' in thescale:
                    avgrisk = thescale['commonriskscale'][1][np.searchsorted(thescale['commonriskscale'][0], age)]
                    minrisk = thescale['commonriskscale'][2][np.searchsorted(thescale['commonriskscale'][0], age)]
                    return [myrisk, avgrisk, minrisk]
                else:
                    None
            else:
                return None
        return None
    # 缺血性心血管病icvd十年发病风险评估
    # 参数： userdata-用户的基础数据   
    # 返回结果：用户的得分                 
    def icvdassess(self,userdata):
        #总分赋初值0
        tatol = 0  
        #计算最近3天的平均值
        daynum=3  
        
        #计算年龄       
        age = userdata.getage()
        sex = userdata.getsex()
        
        if (age is not None) and (sex is not None):
            #年龄分值计算
            score = self.getvalscale(sex=sex, htype='agescale', val=age)
            tatol += score
            #吸烟评分
            smoke=userdata.getsmoke()    
            if smoke is not None:
                score = self.getboolscale(sex=sex, htype='smokescale', val=smoke)
                tatol += score
            else:
                return None
            #糖尿病评分
            diabetes=userdata.getdiabetes() 
            if diabetes is not None:
                score = self.getboolscale(sex=sex, htype='diabetesscale', val=diabetes)
                tatol += score
            else:
                return None
            #BMI分值计算,计算最近身高、体重、腰围平均值，计算平均值BMI
            bodyinfoavg=userdata.getbodyinfoavg(num=daynum)
            bmi = bodyinfoavg[1] * 10000 / bodyinfoavg[0] / bodyinfoavg[0]
            #返回BMI的分值
            score = self.getvalscale(sex=sex, htype='weightscale', val=bmi)
            if score is not None:
                tatol += score
            else:
                return None

            #血压分值计算，计算最近三天血压平均值
            bloodpressureavg = userdata.getbloodpressureavg(num=daynum)
            #返回血压的分值
            score = self.getvalscale(sex=sex, htype='bloodppressurescale', val=bloodpressureavg[0])
            if score is not None:
                tatol += score
            else:
                return None

            #血脂分值计算，计算最近三天血脂平均值
            bcholesterinavg = userdata.getbcholesterinavg(num=daynum)
            #返回血脂的分值
            score = self.getvalscale(sex=sex, htype='tcscale', val=bcholesterinavg[0])
            if score is not None:
                tatol += score
            else:
                return None

            return self.geticvd(sex, age, tatol)
    # 获取健康风险分析结果
    # 参数： hmtypename-风险类型   
    # 返回结果：风险分析结果列表  
    def getrisks(self,hmtypename):  
        hmtype=Indicator.objects.filter(name=hmtypename).first()
        risks= np.array(RiskAnalyse.objects.filter(hmtype=hmtype).values_list('risk'))
        return risks
    # 获取健康风险干预建议结果
    # 参数： hmtypename-风险类型   
    # 返回结果：风险干预建议结果列表 
    def getintervents(self,hmtypename): 
        hmtype=Indicator.objects.filter(name=hmtypename).first()
        intervents= np.array(HealthIntervent.objects.filter(hmtype=hmtype).values_list('intervent'))
        return intervents
