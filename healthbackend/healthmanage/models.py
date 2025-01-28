from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class UserInfo(models.Model):
    Userinfo_sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user=models.OneToOneField(User,unique=True,verbose_name='Username',on_delete=models.CASCADE)
    ssn =  models.CharField(verbose_name='ID Number',max_length=18,null=True) 
    birthday = models.DateField(verbose_name='BirthDay')
    sex = models.CharField(verbose_name='Gender',default='M',choices=Userinfo_sex_choice,max_length=1,db_index=True)
    phone = models.CharField(verbose_name='Phone',max_length=11)
    province = models.CharField(verbose_name='Province', max_length=16,default='Liaoning',db_index=True)
    city = models.CharField(verbose_name='City', max_length=16,default='Shenyang')
    org = models.CharField(verbose_name='Company', max_length=30,null=True,blank=True,default=None)
    job = models.CharField(verbose_name='Position', max_length=20,default='Engineer')
    address = models.CharField(verbose_name='Address', max_length=60,null=True,default=None)
    photo = models.ImageField(verbose_name='Photo',blank=True,default=None)

    def __str__(self):
        return '%s--%s' % (self.user, self.ssn)

    class Meta:
        verbose_name = 'Basic Info'
        verbose_name_plural = "Basic Info"

class SmokeDiabetesInfo(models.Model):
    user=models.OneToOneField(User,unique=True,verbose_name='Usename',on_delete=models.CASCADE)
    smoke= models.BooleanField(verbose_name='Smoke',default=False,db_index=True)
    smokestart = models.DateField(verbose_name='Smoke Startime',null=True,blank=True,default=None)
    drink= models.BooleanField(verbose_name='Drinking',default=False,db_index=True)
    drinkstart = models.DateField(verbose_name='Drinking Startime',null=True,blank=True,default=None)
    diabetes=models.BooleanField(verbose_name='Diabetes',default=False,db_index=True)
    diabetesstart = models.DateField(verbose_name='Diabetes Startime',null=True,blank=True,default=None)

    def __str__(self):
        return '%s:%s--%s' % (self.user, self.smoke,self.diabetes)

    class Meta:
        verbose_name = 'Drinking&Diabetes Info'
        verbose_name_plural = "Drinking&Diabetes Info"

class BodyInfo(models.Model):
    user=models.ForeignKey(User,verbose_name='User',on_delete=models.CASCADE)
    measuretime = models.DateTimeField(verbose_name='Measure Time',unique=True)
    height =  models.DecimalField(verbose_name=('Height(cm)'),max_digits=5,decimal_places=2) 
    weight =  models.DecimalField(verbose_name=('Weight(kg)'),max_digits=5,decimal_places=2) 
    waist =  models.DecimalField(verbose_name=('Waist(cm)'),max_digits=4,decimal_places=2) 
    def __str__(self):
        return '%s:%s-%s' % (self.user, self.height,self.weight)

    class Meta:
        unique_together = ('user', 'measuretime')
        ordering = ['user', '-measuretime']
        verbose_name = 'Height&Weight Info'
        verbose_name_plural = "Height&Weight Info"

class BloodPressure(models.Model):
    user=models.ForeignKey(User,verbose_name='User',on_delete=models.CASCADE)
    measuretime = models.DateTimeField(verbose_name='Measure Time',unique=True)
    DBP =  models.SmallIntegerField(verbose_name='DBP(mmHg)') 
    SBP =  models.SmallIntegerField(verbose_name='SBP(mmHg)') 
    HR =  models.SmallIntegerField(verbose_name='Heart Rate') 
    def __str__(self):
        return '%s:%s-%s' % (self.user, self.DBP,self.SBP)

    class Meta:
        unique_together = ('user', 'measuretime')
        ordering = ['user', '-measuretime']
        verbose_name = 'Blood Pressure Info'
        verbose_name_plural = "Blood Pressure Info"

class Bcholesterin(models.Model):
    user=models.ForeignKey(User,verbose_name='User',on_delete=models.CASCADE)
    measuretime = models.DateTimeField(verbose_name='Measure Time',unique=True)
    TC =  models.DecimalField(verbose_name='TC(mmol/L)',max_digits=4,decimal_places=2) 
    LDL =  models.DecimalField(verbose_name='LDL(mmol/L)',max_digits=4,decimal_places=2) 
    HDL =  models.DecimalField(verbose_name='HDL(mmol/L)',max_digits=4,decimal_places=2) 
    TG =  models.DecimalField(verbose_name='TG(mmol/L)',max_digits=4,decimal_places=2) 
    
    def __str__(self):
        return '%s:%s-%s' % (self.user, self.TC,self.TG)

    class Meta:
        # 数据库中生成的表名称 默认 app名称 + 下划线 + 类名
        #db_table = "table_name"
        #排序
        ordering = ['user', '-measuretime']
        # 联合索引
        #index_together = [('user', 'measuretime'),]
        # 联合唯一索引
        unique_together = ('user', 'measuretime')
        # admin中显示的表名称
        verbose_name = 'Blood Lipid Info'
        verbose_name_plural = "Blood Lipid Info"

class Indicator(models.Model):
    name = models.CharField('Indicator Name', max_length=30, unique=True)
    parent = models.ForeignKey('self', verbose_name='Upper Class', null=True, blank=True,on_delete=models.CASCADE, related_name='parents')

    class Meta:
        #db_table = 'health_Indicator'
        ordering = ['parent_id','name'] 
        verbose_name = verbose_name_plural = 'Health Indicators'

#    class MPTTMeta:
#        parent_attr = 'parent'

    def __str__(self):
        return '%s' % (self.name)

class AgeScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender',default='M',choices=sex_choice,max_length=1)
    maxv =  models.SmallIntegerField(verbose_name='Max Age') 
    score =  models.SmallIntegerField(verbose_name='Score') 
    def __str__(self):
        return '%s-%s: %s' % (self.sex, self.score, self.maxv)

    class Meta:
        ordering = ['sex', 'maxv']
        unique_together = ('sex', 'maxv')
        verbose_name = 'ICVD Age Criteria'
        verbose_name_plural = "ICVD Age Criteria"

class WeightScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender',default='M',choices=sex_choice,max_length=1)
    maxv =  models.SmallIntegerField(verbose_name='BMI Max Value') 
    score =  models.SmallIntegerField(verbose_name='Score') 
    def __str__(self):
        return '%s-%s: %s' % (self.sex, self.score, self.maxv)

    class Meta:
        ordering = ['sex', 'maxv']
        unique_together = ('sex', 'maxv')
        verbose_name = 'ICVD Weight Criteria'
        verbose_name_plural = "ICVD Weight Criteria"



class BloodPressureScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender',default='M',choices=sex_choice,max_length=1)
    maxv =  models.SmallIntegerField(verbose_name='SBP Max Value') 
    score =  models.SmallIntegerField(verbose_name='Score') 
    def __str__(self):
        return '%s-%s:%s' % (self.sex, self.score, self.maxv)

    class Meta:
        ordering = ['sex', 'maxv']
        unique_together = ('sex', 'maxv')
        verbose_name = 'ICVD Blood Pressure Criteria'
        verbose_name_plural = "ICVD Blood Pressure Criteria"

class TCScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender',default='M',choices=sex_choice,max_length=1)
    maxv =  models.DecimalField(verbose_name='Max cholesterol',max_digits=4,decimal_places=2)
    score =  models.SmallIntegerField(verbose_name='Score') 
    def __str__(self):
        return '%s-%s: %s' % (self.sex, self.score,self.maxv)

    class Meta:
        ordering = ['sex', 'maxv']
        unique_together = ('sex', 'maxv')
        verbose_name = 'ICVD Blood Lipid Criteria'
        verbose_name_plural = "ICVD Blood Lipid Criteria"



class SmokeScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender',default='M',choices=sex_choice,max_length=1)
    smoke =  models.BooleanField(verbose_name='Whether Smoke') 
    score =  models.SmallIntegerField(verbose_name='Score') 
    def __str__(self):
        return '%s-%s:%s' % (self.sex, self.smoke, self.score)

    class Meta:
        ordering = ['sex', 'smoke']
        unique_together = ('sex', 'smoke')
        verbose_name = 'ICVD Smoke Criteria'
        verbose_name_plural = "ICVD Smoke Criteria"

class DiabetesScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender', default='M', choices=sex_choice, max_length=1)
    diabetes =  models.BooleanField(verbose_name='Whether Diabetes') 
    score =  models.SmallIntegerField(verbose_name='Score') 
    def __str__(self):
        return '%s-%s:%s' % (self.sex, self.diabetes, self.score)

    class Meta:
        ordering = ['sex', 'diabetes']
        unique_together = ('sex', 'diabetes') 
        verbose_name = 'ICVD Diabetes Criteria'
        verbose_name_plural = "ICVD Diabetes Criteria"

class RiskEvaluatScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender',default='M',choices=sex_choice,max_length=1)
    score =  models.SmallIntegerField(verbose_name='Score') 
    risk =  models.DecimalField(verbose_name=('Rsik Value%'),max_digits=3,decimal_places=1) 
    def __str__(self):
        return '%s:%s-%s' % (self.sex, self.score, self.risk)

    class Meta:
        ordering = ['sex', 'score']
        unique_together = ('sex', 'score')
        verbose_name = 'ICVD 10-Year Criteria'
        verbose_name_plural = "ICVD 10-Year Criteria"

class CommonRiskScale(models.Model):
    sex_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(verbose_name='Gender',default='M',choices=sex_choice,max_length=1)
    age =  models.SmallIntegerField(verbose_name='Age') 
    avgrisk =  models.DecimalField(verbose_name=('Average Risk%'),max_digits=3,decimal_places=1) 
    minrisk =  models.DecimalField(verbose_name=('Min Risk%'),max_digits=3,decimal_places=1) 
    def __str__(self):
        return '%s-%s :%s %s' % (self.sex, self.age, self.avgrisk, self.minrisk)

    class Meta:
        ordering = ['sex', 'age']
        unique_together = ('sex', 'age')
        verbose_name = 'ICVD 10-Year Standard Criteria'
        verbose_name_plural = "ICVD 10-Year Standard Criteria"

class BMIScale(models.Model):
    bmi =  models.DecimalField(verbose_name='BMI Value',max_digits=4,decimal_places=2)
    wtype = models.ForeignKey(Indicator, verbose_name='Weight Classification', on_delete=models.CASCADE)
    def __str__(self):
        return '%s: %s' % (self.wtype, self.bmi)

    class Meta:
        ordering = ['bmi', 'wtype']
        verbose_name = verbose_name_plural ='BMI Criteria'

class SingleAssess(models.Model):
    assesstype =models.CharField(verbose_name='Indicator Type',max_length=30)
    assessname = models.CharField(verbose_name='Indicator Criteria',max_length=30)
    minv =  models.FloatField(verbose_name='Min Indicator Criteria') 
    maxv =  models.FloatField(verbose_name='Max Indicator Criteria')
    def __str__(self):
        return '%s:%s' % (self.assesstype, self.assessname)

    class Meta:
        ordering = ['assesstype', 'assessname','minv']
        unique_together = ('assesstype', 'assessname')
        verbose_name = verbose_name_plural ='Single Indicator Criteria'

class RiskAnalyse(models.Model):
    hmtype =models.ForeignKey(Indicator, verbose_name='Risk Types', on_delete=models.CASCADE)
    risk =  models.CharField(verbose_name='Risk',max_length=254) 
  
    def __str__(self):
        return '%s' % (self.hmtype)
    class Meta:
        verbose_name = verbose_name_plural = "Health Risk Analysis"

class HealthIntervent(models.Model):
    hmtype =models.ForeignKey(Indicator, verbose_name='Risk Types', on_delete=models.CASCADE)
    intervent =  models.CharField(verbose_name='Intervene Suggestions',max_length=254) 
    def __str__(self):
        return '%s' % (self.hmtype)

    class Meta:
        verbose_name = 'Intervene Suggestions'
        verbose_name_plural = "Intervene Suggestions"


