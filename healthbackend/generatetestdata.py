#!/usr/bin/env python
#coding:utf-8
 
import os
import random
import datetime
import django

from django.conf import settings
from django.utils import timezone
from faker import Faker
from dateutil.relativedelta import relativedelta

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client
from tencentcloud.tmt.v20180321 import models as tmt_models
 
SecretId = os.environ.get('SECRET_ID')
SecretKey = os.environ.get('SECRET_KEY')

#locale='nl_NL'
#locale='en_US'
locale='zh_CN'

fake = Faker(locale=locale)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthbackend.settings")
django.setup()
from django.contrib.auth.models import User
from django.contrib.auth.models import Group,Permission

from healthmanage.models import *

if settings.LANGUAGE_CODE == 'en':
    citys = {
        'Beijing': ['Beijing'],
        'Guangdong': ['Guangzhou', 'Shenzhen', 'Zhuhai', 'Shantou', 'Shaoguan', 'Foshan', 'Jiangmen', 'Zhanjiang', 'Maoming', 'Zhaoqing', 'Huizhou', 'Meizhou', 'Shanwei', 'Heyuan', 'Yangjiang', 'Qingyuan', 'Dongguan', 'Zhongshan', 'Chaozhou', 'Jieyang', 'Yunfu'],
        'Shanghai': ['Shanghai'],
        'Tianjin': ['Tianjin'],
        'Chongqing': ['Chongqing'],
        'Liaoning': ['Shenyang', 'Dalian', 'Anshan', 'Fushun', 'Benxi', 'Dandong', 'Jinzhou', 'Yingkou', 'Fuxin', 'Liaoyang', 'Panjin', 'Tieling', 'Chaoyang', 'Huludao'],
        'Jiangsu': ['Nanjing', 'Suzhou', 'Wuxi', 'Changzhou', 'Zhenjiang', 'Nantong', 'Taizhou', 'Yangzhou', 'Yancheng', 'Lianyungang', 'Xuzhou', "Huai'an", 'Suqian'],
        'Hubei': ['Wuhan', 'Huangshi', 'Shiyan', 'Jingzhou', 'Yichang', 'Xiangyang', 'Ezhou', 'Jingmen', 'Xiaogan', 'Huanggang', 'Xianning', 'Suizhou', 'Enshi Tujia and Miao Autonomous Prefecture', 'Xiantao', 'Tianmen', 'Qianjiang', 'Shennongjia Forestry District'],
        'Sichuan': ['Chengdu', 'Zigong', 'Panzhihua', 'Luzhou', 'Deyang', 'Mianyang', 'Guangyuan', 'Suining', 'Neijiang', 'Leshan', 'Nanchong', 'Meishan', 'Yibin', "Guang'an", 'Dazhou', 'Yaan', 'Bazhong', 'Ziyang', 'Aba Tibetan and Qiang Autonomous Prefecture', 'Ganzi Tibetan Autonomous Prefecture', 'Liangshan Yi Autonomous Prefecture'],
        'Shaanxi': ["Xi'an", 'Tongchuan', 'Baoji', 'Xianyang', 'Weinan', "Yan'an", 'Hanzhong', 'Yulin', 'Ankang', 'Shangluo'],
        'Hebei': ['Shijiazhuang', 'Tangshan', 'Qinhuangdao', 'Handan', 'Xingtai', 'Baoding', 'Zhangjiakou', 'Chengde', 'Cangzhou', 'Langfang', 'Hengshui'],
        'Shanxi': ['Taiyuan', 'Datong', 'Yangquan', 'Changzhi', 'Jincheng', 'Shuozhou', 'Jinzhong', 'Yuncheng', 'Xinzhou', 'Linfen', 'Lvliang'],
        'Henan': ['Zhengzhou', 'Kaifeng', 'Luoyang', 'Pingdingshan', 'Anyang', 'Hebi', 'Xinxiang', 'Jiaozuo', 'Puyang', 'Xuchang', 'Luohe', 'Sanmenxia', 'Nanyang', 'Shangqiu', 'Xinyang', 'Zhoukou', 'Zhumadian'],
        'Jilin': ['Changchun', 'Jilin', 'Siping', 'Liaoyuan', 'Tonghua', 'Baishan', 'Songyuan', 'Baicheng', 'Yanbian Korean Autonomous Prefecture'],
        'Heilongjiang': ['Harbin', 'Qiqihaer', 'Hegang', 'Shuangyashan', 'Jixi', 'Daqing', 'Yichun', 'Mudanjiang', 'Jiamusi', 'Qitaihe', 'Heihe', 'Suihua', "Daxing'anling Prefecture"],
        'Inner Mongolia': ['Hohhot', 'Baotou', 'Wuhai', 'Chifeng', 'Tongliao', 'Ordos', 'Hulunbuir', 'Bayannur', 'Ulanqab', 'Xilingol League', "Xing'an League", 'Alxa League'],
        'Shandong': ['Jinan', 'Qingdao', 'Zibo', 'Zaozhuang', 'Dongying', 'Yantai', 'Weifang', 'Jining', "Tai'an", 'Weihai', 'Rizhao', 'Laizhou', 'Linyi', 'Dezhou', 'Liaocheng', 'Binzhou', 'Heze'],
        'Anhui': ['Hefei', 'Wuhu', 'Bengbu', 'Huainan', 'Maanshan', 'Huaibei', 'Tongling', 'Anqing', 'Huangshan', 'Chuzhou', 'Fuyang', 'Suzhou', 'Chaohu', 'Liuan', 'Bozhou', 'Chizhou', 'Xuancheng'],
        'Zhejiang': ['Hangzhou', 'Ningbo', 'Wenzhou', 'Jiaxing', 'Huzhou', 'Shaoxing', 'Jinhua', 'Quzhou', 'Zhoushan', 'Taizhou', 'Lishui'],
        'Fujian': ['Fuzhou', 'Xiamen', 'Putian', 'Sanming', 'Quanzhou', 'Zhangzhou', 'Nanping', 'Longyan', 'Ningde'],
        'Hunan': ['Changsha', 'Zhuzhou', 'Xiangtan', 'Hengyang', 'Shaoyang', 'Yueyang', 'Changde', 'Zhangjiajie', 'Yiyang', 'Chenzhou', 'Yongzhou', 'Huaihua', 'Loudi', 'Xiangxi Tujia and Miao Autonomous Prefecture'],
        'Guangxi': ['Nanning', 'Liuzhou', 'Guilin', 'Wuzhou', 'Beihai', 'Fangchenggang', 'Qinzhou', 'Guigang', 'Yulin', 'Baise', 'Hezhou', 'Hechi', 'Laibin', 'Chongzuo'],
        'Jiangxi': ['Nanchang', 'Jingdezhen', 'Pingxiang', 'Jiujiang', 'Xinyu', 'Yingtan', 'Ganzhou', "Ji'an", 'Yichun', 'Fuzhou', 'Shangrao'],
        'Guizhou': ['Guiyang', 'Liupanshui', 'Zunyi', 'Anshun', 'Tongren Prefecture', 'Bijie Prefecture', 'Qianxinan Buyi and Miao Autonomous Prefecture', 'Qiandongnan Miao and Dong Autonomous Prefecture', 'Qiannan Buyi and Miao Autonomous Prefecture'],
        'Yunnan': ['Kunming', 'Qujing', 'Yuxi', 'Baoshan', 'Zhaotong', 'Lijiang', "Pu'er", 'Lincang', 'Dehong Dai and Jingpo Autonomous Prefecture', 'Nujiang Lisu Autonomous Prefecture', 'Diqing Tibetan Autonomous Prefecture', 'Dali Bai Autonomous Prefecture', 'Chuxiong Yi Autonomous Prefecture', 'Honghe Hani and Yi Autonomous Prefecture', 'Wenshan Zhuang and Miao Autonomous Prefecture', 'Xishuangbanna Dai Autonomous Prefecture'],
        'Tibet': ['Lhasa', 'Nagqu Prefecture', 'Qamdo Prefecture', 'Nyingchi Prefecture', 'Shannan Prefecture', 'Xigaze Prefecture', 'Ali Prefecture'],
        'Hainan': ['Haikou', 'Sanya', 'Wuzhishan', 'Qionghai', 'Danzhou', 'Wenchang', 'Wanning', 'Dongfang', 'Chengmai County', "Ding'an County", 'Tunchang County', 'Lingao County', 'Baisha Li Autonomous County', 'Changjiang Li Autonomous County', 'Ledong Li Autonomous County', 'Lingshui Li Autonomous County', 'Baoting Li and Miao Autonomous County', 'Qiongzhong Li and Miao Autonomous County'],
        'Gansu': ['Lanzhou', 'Jiayuguan', 'Jinchang', 'Baiyin', 'Tianshui', 'Wuwei', 'Jiuquan', 'Zhangye', 'Qingyang', 'Pingliang', 'Dingxi', 'Longnan', 'Linxia Hui Autonomous Prefecture', 'Gannan Tibetan Autonomous Prefecture'],
        'Ningxia': ['Yinchuan', 'Shizuishan', 'Wuzhong', 'Guyuan', 'Zhongwei'],
        'Qinghai': ['Xining', 'Haidong Prefecture', 'Haibei Tibetan Autonomous Prefecture', 'Hainan Tibetan Autonomous Prefecture', 'Huangnan Tibetan Autonomous Prefecture', 'Golog Tibetan Autonomous Prefecture', 'Yushu Tibetan Autonomous Prefecture', 'Haixi Mongol and Tibetan Autonomous Prefecture'],
        'Xinjiang': ['Urumqi', 'Karamay', 'Turpan Prefecture', 'Hami Prefecture', 'Hotan Prefecture', 'Aksu Prefecture', 'Kashgar Prefecture', 'Kizilsu Kirgiz Autonomous Prefecture', 'Bayingolin Mongol Autonomous Prefecture', 'Changji Hui Autonomous Prefecture', 'Bortala Mongol Autonomous Prefecture', 'Shihezi', 'Aral', 'Tumushuke', 'Wujiaqu', 'Ili Kazak Autonomous Prefecture'],
        'Hong Kong': ['Hong Kong'],
        'Macau': ['Macau'],
        'Taiwan': ['Taipei City', 'Kaohsiung City', 'Taipei County', 'Taoyuan County', 'Hsinchu County', 'Miaoli County', 'Taichung County', 'Changhua County', 'Nantou County', 'Yunlin County', 'Chiayi County', 'Tainan County', 'Kaohsiung County', 'Pingtung County', 'Yilan County', 'Hualien County', 'Taitung County', 'Penghu County', 'Keelung City', 'Hsinchu City', 'Taichung City', 'Chiayi City', 'Tainan City']
    }

else:
    citys = { '北京': ['北京'],    
                '广东': ['广州', '深圳', '珠海', '汕头', '韶关', '佛山', '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮'],    
                '上海': ['上海'],    
                '天津': ['天津'],    
                '重庆': ['重庆'],    
                '辽宁': ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛'],    
                '江苏': ['南京', '苏州', '无锡', '常州', '镇江', '南通', '泰州', '扬州', '盐城', '连云港', '徐州', '淮安', '宿迁'],    
                '湖北': ['武汉', '黄石', '十堰', '荆州', '宜昌', '襄樊', '鄂州', '荆门', '孝感', '黄冈', '咸宁', '随州', '恩施土家族苗族自治州', '仙桃', '天门', '潜江', '神农架林区'],
                '四川': ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州'], 
                '陕西': ['西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'],    
                '河北': ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水'],    
                '山西': ['太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'],    
                '河南': ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店'],    
                '吉林': ['长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边朝鲜族自治州'],    
                '黑龙江': ['哈尔滨', '齐齐哈尔', '鹤岗', '双鸭山', '鸡西', '大庆', '伊春', '牡丹江', '佳木斯', '七台河', '黑河', '绥化', '大兴安岭地区'],    
                '内蒙古': ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '锡林郭勒盟', '兴安盟', '阿拉善盟'],    
                '山东': ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '莱芜', '临沂', '德州', '聊城', '滨州', '菏泽'],    
                '安徽': ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '巢湖', '六安', '亳州', '池州', '宣城'],    
                '浙江': ['杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水'],    
                '福建': ['福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德'],    
                '湖南': ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西土家族苗族自治州'],    
                '广西': ['南宁', '柳州', '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左'],    
                '江西': ['南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶'],    
                '贵州': ['贵阳', '六盘水', '遵义', '安顺', '铜仁地区', '毕节地区', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州'],    
                '云南': ['昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '德宏傣族景颇族自治州', '怒江傈僳族自治州', '迪庆藏族自治州', '大理白族自治州', '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州'],    
                '西藏': ['拉萨', '那曲地区', '昌都地区', '林芝地区', '山南地区', '日喀则地区', '阿里地区'],    
                '海南': ['海口', '三亚', '五指山', '琼海', '儋州', '文昌', '万宁', '东方', '澄迈县', '定安县', '屯昌县', '临高县', '白沙黎族自治县', '昌江黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县'],    
                '甘肃': ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '酒泉', '张掖', '庆阳', '平凉', '定西', '陇南', '临夏回族自治州', '甘南藏族自治州'],    
                '宁夏': ['银川', '石嘴山', '吴忠', '固原', '中卫'],    
                '青海': ['西宁', '海东地区', '海北藏族自治州', '海南藏族自治州', '黄南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州'],    
                '新疆': ['乌鲁木齐', '克拉玛依', '吐鲁番地区', '哈密地区', '和田地区', '阿克苏地区', '喀什地区', '克孜勒苏柯尔克孜自治州', '巴音郭楞蒙古自治州', '昌吉回族自治州', '博尔塔拉蒙古自治州', '石河子', '阿拉尔', '图木舒克', '五家渠', '伊犁哈萨克自治州'],    
                '香港': ['香港'],    
                '澳门': ['澳门'],    
                '台湾': ['台北市', '高雄市', '台北县', '桃园县', '新竹县', '苗栗县', '台中县', '彰化县', '南投县', '云林县', '嘉义县', '台南县', '高雄县', '屏东县', '宜兰县', '花莲县', '台东县', '澎湖县', '基隆市', '新竹市', '台中市', '嘉义市', '台南市']}

#随机生成用户数据
#参数：num-生成用户的数量，days-生成数据的天数
#locale='nl_NL'
#locale='en_US'
locale='zh_CN'


fake = Faker(locale=locale)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthbackend.settings")
django.setup()

class TencentTranslate():
    
    '''
    翻译接口，输入为待翻译句子的列表
    '''
    def translate(self, SourceText):
        try: 
            cred = credential.Credential(SecretId, SecretKey)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile) 

            req = tmt_models.TextTranslateRequest()
            req.SourceText = SourceText
            req.Source = "zh"
            req.Target = "en"
            req.ProjectId = 0

            resp = client.TextTranslate(req) 
            return resp.TargetText

        except TencentCloudSDKException as err: 
            print(err)
            return None 
        
def createuserdata(num,days,t):

    while num > 0:

        username = fake.user_name()
        if len(username)<8:
            username += str(fake.random_number(digits=(8-len(username))))

        if User.objects.filter(username=username).count()!=0:
            num = num - 1
            sex = random.choice(('M', 'F'))
            if sex=='M':
                firstname = fake.first_name_male()
            else:
                firstname = fake.first_name_female()
            lastname = fake.last_name()
            if settings.LANGUAGE_CODE == 'en':
                firstname = t.translate(firstname)
                firstname.capitalize()
                lastname = t.translate(lastname)     
                lastname.capitalize()       
            ssn=fake.ssn()
            if locale=='zh_CN':
                birthday =datetime.datetime.strptime(ssn[6:14], '%Y%m%d')
                province = random.choice(list(citys.keys()))
                city=random.choice(citys[province])
            else:
                birthday =fake.date_between(start_date="-30y", end_date="now")-relativedelta(years=fake.random_int(max=80,min=30))
                #birthday =fake.date_of_birth()
                province = fake.country()
                city = fake.city()
            #birthday = fake.date_between(start_date="-50y", end_date="now")-relativedelta(years=fake.random_int(max=80,min=30))
            email=fake.email()

            if settings.LANGUAGE_CODE == 'en' and locale=='zh_CN':
                job = t.translate(fake.job())
                address = t.translate(fake.address())
                org = t.translate(fake.company())
            else:
                job=fake.job()
                address = fake.address()
                org = fake.company()
            phone = fake.phone_number()


            print(ssn,username,lastname,firstname,sex,birthday,email,phone,address,org,province,city,job)

            #注册用户
            user=User.objects.create_user(username=username,password='health123',email=email,last_name=lastname,first_name=firstname,is_staff=True,) 
            if settings.LANGUAGE_CODE == 'en':
                group = Group.objects.get(name='Personal User')
            else:
                group = Group.objects.get(name='个人用户') 
            group.user_set.add(user)

            
            #生成用户信息
            userinfo=UserInfo(user=user,ssn=ssn,sex=sex,birthday=birthday,phone=phone,org=org,job=job,province=province,city=city,address=address)
            userinfo.save()
            max=datetime.date.today().year - birthday.year
            if max < 15:
                smoke=False
                drink=False
            else:
                smoke = random.choice((True, False))
                drink = random.choice((True, False))
            if smoke:
                smokestart = birthday + relativedelta(years=fake.random_int(max=max, min=1))
            else:
                smokestart = None
            if drink:
                drinkstart = birthday + relativedelta(years=fake.random_int(max=max, min=1))
            else:
                drinkstart = None
            diabetes = random.choice((True, False))
            if diabetes:
                diabetesstart = birthday + relativedelta(years=fake.random_int(max=datetime.date.today().year - birthday.year, min=0))
            else:
                diabetesstart = None
            smokediabetes = SmokeDiabetesInfo(user=user, smokestart=smokestart, smoke=smoke, \
                drink =drink,drinkstart =drinkstart,diabetesstart=diabetesstart,diabetes=diabetes)
            smokediabetes.save()


            startdate=timezone.now()
            #生成身高体重数据
            v1 = fake.random_int(max=199,min=150) 
            bmi=random.uniform(14,45)
            v2 =  v1/100*v1/100*bmi
            nomalheight = pow(v2 / bmi, 0.5) * 100
            
            v3 = fake.random_int(max=105,min=95)*0.42*nomalheight/100
            i=0
            while i<days:
                curdate= startdate-relativedelta(days=i)
                i += 1
                x1 = v1+random.random()*random.choice((-1,1))
                x2 = v2+ random.uniform(0,3)*random.choice((-1,1))
                x3 = v3+ random.uniform(0,3)*random.choice((-1,1))
                print(curdate,x1,x2,x3)
                modobj=BodyInfo(user=user,measuretime=curdate,height = x1,weight =x2,waist = x3)
                modobj.save()
            #生成血压数据
            v1 = fake.random_int(max=220,min=70) 
            v2 = v1-fake.random_int(max=50,min=30) 
            v3 = fake.random_int(max=99,min=40)
            i=0
            while i<days:
                curdate= startdate-relativedelta(days=i)
                i += 1
                x1 = v1+random.randint(0,10)*random.choice((-1,1))
                x2 = v2+random.randint(0,10)*random.choice((-1,1))
                x3 = v3+random.randint(0,5)*random.choice((-1,1))
                print(curdate,x1,x2,x3)
                modobj=BloodPressure(user=user,measuretime=curdate,DBP = x1,SBP =x2,HR = x3)
                modobj.save()

            #生成血脂数据
            v1 = random.uniform(0.15,4)
            v2 = random.uniform(1.5,6.5) 
            v3 = random.uniform(0.8,2)
            v4 = random.uniform(0.3,2.2)
            i=0
            while i<days:
                curdate= startdate-relativedelta(months=i)
                i += 1
                x1 = v1+random.uniform(0.015,0.2)*random.choice((-1,1))
                x2 = v2+random.uniform(0.15,0.4)*random.choice((-1,1))
                x3 = v3+random.uniform(0.02,0.2)*random.choice((-1,1))
                x4 = v4+random.uniform(0.03,0.2)*random.choice((-1,1))
                modobj=Bcholesterin(user=user,measuretime=curdate,LDL = x1,TC =x2,HDL = x3,TG = x4)
                modobj.save()

def createscale():
    print("清除所有评价标准表数据")
    AgeScale.objects.all().delete()
    WeightScale.objects.all().delete()
    BloodPressureScale.objects.all().delete()
    TCScale.objects.all().delete()
    RiskEvaluatScale.objects.all().delete()
    CommonRiskScale.objects.all().delete()
    SmokeScale.objects.all().delete()
    DiabetesScale.objects.all().delete()
    BMIScale.objects.all().delete()
    RiskAnalyse.objects.all().delete()
    HealthIntervent.objects.all().delete()
    SingleAssess.objects.all().delete()
    Indicator.objects.all().delete()

    print("增加 {} 数据".format(Indicator._meta.verbose_name))
    if settings.LANGUAGE_CODE == 'en':
        parents=['Risk factors','BMI evaluation']
        childs=[['Smoking','Risk factors'],
                ['Drinking','Risk factors'],
                ['Diabetes','Risk factors'],
                ['Underweight','Risk factors'],
                ['Obesity','Risk factors'],
                ['Under weight','BMI evaluation'],
                ['Normal weight','BMI evaluation'],
                ['Over weight','BMI evaluation'],
                ['Grade I obesity','BMI evaluation'],
                ['Grade II obesity','BMI evaluation'],
                ['Grade III obesity','BMI evaluation'],
                ['Hypotension','Risk factors'],
                ['Hypertension','Risk factors'],        
                ['Hyperlipidemia','Risk factors'],
                ['Hypolipidemia','Risk factors'],
                ['Tachycardia','Risk factors'],
                ['Bradycardia','Risk factors'],]
    else:
        parents=['危险因素','BMI评价']
        childs=[['吸烟','危险因素'],
                ['饮酒','危险因素'],
                ['糖尿病','危险因素'],
                ['体重消瘦','危险因素'],
                ['体重肥胖','危险因素'],
                ['体重偏瘦','BMI评价'],
                ['体重正常','BMI评价'],
                ['体重偏胖','BMI评价'],
                ['I度肥胖','BMI评价'],
                ['II度肥胖','BMI评价'],
                ['III度肥胖','BMI评价'],
                ['低血压','危险因素'],
                ['高血压','危险因素'],        
                ['高脂血','危险因素'],
                ['低脂血','危险因素'],
                ['心动过速','危险因素'],
                ['心动过缓','危险因素'],]
    for parent in parents:
        Indicator.objects.get_or_create(name=parent)
    for child in childs:
        id=Indicator.objects.filter(name=child[1]).first()
        Indicator.objects.get_or_create(name=child[0],parent=id)

    print("增加 {} 数据".format(AgeScale._meta.verbose_name))
    lines = [
        ['M',40,0],
        ['M',45,1],
        ['M',50,2],
        ['M',55,3],
        ['M',60,4],
        ['M',65,5],
        ['M',70,6],
        ['M',75,7],
        ['M',80,8],
        ['M',85,9],
        ['M',90,10],
        ['M',95,11],
        ['M',120,12],
        ['F',40,0],
        ['F',45,1],
        ['F',50,2],
        ['F',55,3],
        ['F',60,4],
        ['F',65,5],
        ['F',70,6],
        ['F',75,7],
        ['F',80,8],
        ['F',85,9],
        ['F',90,10],
        ['F',95,11],
        ['F',120,12]]
    for line in lines:
        AgeScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(WeightScale._meta.verbose_name))
    lines = [
        ['M',24,0],
        ['M',28,1],
        ['M',50,2],
        ['F',24,0],
        ['F',28,1],
        ['F',50,2]]
    for line in lines:
        WeightScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(BloodPressureScale._meta.verbose_name))
    lines = [
        ['M',120,-2],
        ['M',130,0],
        ['M',140,1],
        ['M',160,2],
        ['M',180,5],
        ['M',280,8],
        ['F',120,-2],
        ['F',130,0],
        ['F',140,1],
        ['F',160,2],
        ['F',180,3],
        ['F',280,4]]
    for line in lines:
        BloodPressureScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(TCScale._meta.verbose_name))
    lines = [
        ['M',5.18,0],
        ['M',10,1],
        ['F',5.18,0],
        ['F',10,1]]
    for line in lines:
        TCScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(RiskEvaluatScale._meta.verbose_name))
    lines = [
        ['M',-2,0.2],
        ['M',-1,0.3],
        ['M',0,0.5],
        ['M',1,0.6],
        ['M',2,0.8],
        ['M',3,1.1],
        ['M',4,1.5],
        ['M',5,2.1],
        ['M',6,2.9],
        ['M',7,3.9],
        ['M',8,5.4],
        ['M',9,7.3],
        ['M',10,9.7],
        ['M',11,12.8],
        ['M',12,16.8],
        ['M',13,21.7],
        ['M',14,27.7],
        ['M',15,35.3],
        ['M',16,44.3],
        ['M',17,52.6],
        ['F',-2,0.1],
        ['F',-1,0.2],
        ['F',0,0.2],
        ['F',1,0.3],
        ['F',2,0.5],
        ['F',3,0.8],
        ['F',4,1.2],
        ['F',5,1.8],
        ['F',6,2.8],
        ['F',7,4.4],
        ['F',8,6.8],
        ['F',9,10.3],
        ['F',10,15.6],
        ['F',11,23],
        ['F',12,32.7],
        ['F',13,43.1]]
    for line in lines:
        RiskEvaluatScale.objects.get_or_create(sex = line[0],risk =line[2],score =line[1]) 

    print("增加 {} 数据".format(CommonRiskScale._meta.verbose_name))
    lines = [
        ['M',40,1,0.3],
        ['M',45,1.4,0.4],
        ['M',50,1.9,0.5],
        ['M',55,2.6,0.7],
        ['M',120,3.6,1],
        ['F',40,0.3,0.1],
        ['F',45,0.4,0.1],
        ['F',50,0.6,0.2],
        ['F',55,0.9,0.3],
        ['F',120,1.4,0.5]]
    for line in lines:
        CommonRiskScale.objects.get_or_create(sex = line[0],age =line[1],avgrisk =line[2],minrisk=line[3]) 

    print("增加 {} 数据".format(SmokeScale._meta.verbose_name))
    SmokeScale.objects.get_or_create(sex = 'M',smoke =False,score =0) 
    SmokeScale.objects.get_or_create(sex = 'M',smoke =True,score =2) 
    SmokeScale.objects.get_or_create(sex = 'F',smoke =False,score =0) 
    SmokeScale.objects.get_or_create(sex = 'F',smoke =True,score =1) 

    print("增加 {} 数据".format(DiabetesScale._meta.verbose_name))
    DiabetesScale.objects.get_or_create(sex = 'M',diabetes =False,score =0) 
    DiabetesScale.objects.get_or_create(sex = 'M',diabetes =True,score =1) 
    DiabetesScale.objects.get_or_create(sex = 'F',diabetes =False,score =0) 
    DiabetesScale.objects.get_or_create(sex = 'F', diabetes=True, score=2)

    print("增加 {} 数据".format(BMIScale._meta.verbose_name))
    if settings.LANGUAGE_CODE == 'en':
        lines = [
            ['Under weight',18.5],
            ['Normal weight',24],
            ['Over weight',27],
            ['Grade I obesity',30],
            ['Grade II obesity',40],
            ['Grade III obesity',50]]
    else:    
        lines = [
            ['体重偏瘦',18.5],
            ['体重正常',24],
            ['体重偏胖',27],
            ['I度肥胖',30],
            ['II度肥胖',40],
            ['III度肥胖',50]]

    for line in lines:
        wtype=Indicator.objects.filter(name=line[0]).first()
        BMIScale.objects.get_or_create(wtype = wtype,bmi =line[1]) 

    print("增加 {} 数据".format(SingleAssess._meta.verbose_name))
    if settings.LANGUAGE_CODE == 'en':
        lines = [
            ['Blood pressure','Systolic blood pressure',90,140],
            ['Blood pressure','Diastolic blood pressure',60,90],
            ['Blood pressure','Heart rate',60,100],
            ['Blood lipid', 'Total cholesterol', 2.35, 5.18],
            ['Blood lipid','Low density',0.25,3.11],
            ['Blood lipid','High density',1.16,1.42],
            ['Blood lipid','Triglycerides',0.51,1.7],]
    else:
        lines = [
            ['血压','收缩压',90,140],
            ['血压','舒张压',60,90],
            ['血压','心率',60,100],
            ['血脂', '总胆固醇', 2.35, 5.18],
            ['血脂','低密度',0.25,3.11],
            ['血脂','高密度',1.16,1.42],
            ['血脂','甘油三酯',0.51,1.7],]
    for line in lines:
        SingleAssess.objects.get_or_create(assesstype = line[0],assessname=line[1],minv=line[2],maxv=line[3]) 

    print("增加{}、{}数据".format(RiskAnalyse._meta.verbose_name,HealthIntervent._meta.verbose_name))
    if settings.LANGUAGE_CODE == 'en':
        lines = (
            ("Smoking", "Epidemiological investigations indicate that smoking is one of the important causative factors for lung cancer, especially squamous cell carcinoma and small cell undifferentiated carcinoma. Smoking can reduce the activity of natural killer cells, thus weakening the body's functions of monitoring, killing, and eliminating tumor cells. The incidence of laryngeal cancer in smokers is more than ten times higher than that in non - smokers, and the incidence of bladder cancer increases by 3 times. In addition, smoking is related to the occurrence of lip cancer, tongue cancer, oral cancer, esophageal cancer, gastric cancer, colon cancer, pancreatic cancer, kidney cancer, and cervical cancer. Clinical studies and animal experiments show that the carcinogens in cigarette smoke can also affect the fetus through the placenta, significantly increasing the cancer incidence in the offspring."),
            ("Smoking", "Smoking is a major risk factor for many cardiovascular and cerebrovascular diseases. The incidence of coronary heart disease, hypertension, cerebrovascular diseases, and peripheral vascular diseases in smokers is significantly higher. Statistical data show that 75%% of patients with coronary heart disease and hypertension have a smoking history. The incidence of coronary heart disease in smokers is 3.5 times higher than that in non - smokers, the case - fatality rate of coronary heart disease is 6 times higher in smokers, and the incidence of myocardial infarction is 2 - 6 times higher in smokers. The risk of stroke in smokers is 2 - 3.5 times that in non - smokers. If smoking and hypertension co - exist, the risk of stroke will increase nearly 20 times. In addition, smokers are prone to obliterative arteriosclerosis and obliterative thrombotic arteritis. Smoking can cause chronic obstructive pulmonary disease, leading to cor pulmonale."),
            ("Smoking", "Smoking is one of the main causes of chronic bronchitis, emphysema, and chronic airway obstruction. Experimental studies have found that long - term smoking can damage and shorten the cilia of the bronchial mucosa, affecting the cilia's clearance function. The incidence of chronic bronchitis in smokers is 2 - 4 times higher than that in non - smokers, and it is directly proportional to the amount and duration of smoking. Patients often have chronic cough, expectoration, and dyspnea during activities. Young asymptomatic smokers also have mild impairment of lung function. Chronic obstructive pulmonary disease caused by smoking is prone to spontaneous pneumothorax. Smokers often suffer from chronic pharyngitis and vocal cord inflammation."),
            ("Smoking", "Smoking can increase gastric acid secretion by 91.5%% compared with non - smokers. It can also inhibit the pancreas from secreting sodium bicarbonate, resulting in an increased acid load in the duodenum and triggering ulcers. Nicotine in tobacco can reduce the tension of the pyloric sphincter, making it easier for bile to reflux. This weakens the defensive factors of the gastric and duodenal mucosa, promotes the occurrence of chronic inflammation and ulcers, and delays the healing of existing ulcers. In addition, smoking can reduce the tension of the lower esophageal sphincter, easily causing reflux esophagitis. After tobacco enters the human body, it interferes with the body's absorption of calcium ions, affecting bone density and causing it to decline."),
            ("Drinking", "Long - term and excessive alcohol consumption can damage the cardiovascular system. After drinking, excess glutamate is produced, which can cause cardiac excitement and increased blood pressure. Therefore, people who drink alcohol for a long time are prone to hypertension and cardiovascular diseases. The kidneys are one of the body's detoxification organs, and alcohol can damage the kidneys and digestive system. When alcohol enters the kidneys, the kidneys will directly send water to the bladder without being able to reabsorb it, leading to dehydration. And when a large amount of alcohol enters the gastrointestinal tract, it will irritate the gastric mucosa, causing discomfort. In severe cases, it can lead to gastric ulcers and gastric bleeding."),
            ("Drinking", "Long - term and excessive alcohol consumption damages the human digestive system. Alcohol contains a large amount of ethanol, which is easily absorbed by the body and then decomposed by the liver. Regular drinking can bring a great burden to the liver, cause liver damage, and make people prone to fatty liver and other diseases. After a large amount of alcohol consumption, it will disrupt the body's endocrine system, leading to a decrease in galactose tolerance, an increase in triglyceride synthesis, and an increase in lipid peroxidation. A research report in the international journal BMC Public Health shows that researchers from Umeå University in Sweden found through research that regular and excessive drinking and alcoholism starting from the age of 16 may be directly related to higher glucose concentrations in the blood of women in later life. And a high blood sugar level is a risk factor for type 2 diabetes."),
            ("Drinking", "Long - term and excessive alcohol consumption can damage the human central nervous system, or cause people to experience trance, fatigue, auditory and visual hallucinations, memory loss, and decreased intelligence. Research published in the journal BMJ shows that even moderate alcohol consumption can lead to a decline in chronic brain cognitive levels."),
            ("Diabetes", "Diabetes is a group of metabolic diseases characterized by high blood sugar. High blood sugar is caused by defects in insulin secretion or impairment of its biological action, or both. The long - term presence of high blood sugar in diabetes leads to chronic damage and dysfunction of various tissues, especially the eyes, kidneys, heart, blood vessels, and nerves. Diabetes has obvious genetic heterogeneity and a family - based tendency. 1/4 to 1/2 of patients have a family history of diabetes. Clinically, there are at least more than 60 genetic syndromes that can be accompanied by diabetes."),
            ("Underweight", "Underweight people often have calcium deficiency. And because of the small amount of fat, it is difficult to build muscle, which will affect the function and metabolism of bone cells and easily lead to osteoporosis. Underweight people generally have problems with unbalanced nutrition intake. They have insufficient intake of hematopoietic substances such as iron, folic acid, and vitamin B12, which can develop into anemia."),
            ("Underweight", "It is easy to lead to a decrease in resistance to viruses and fatigue. Insufficient calorie intake leads to the consumption of body fat for energy, causing the movement of cholesterol, resulting in high cholesterol in the bile. The bile becomes viscous, and crystals precipitate and form gallstones."),
            ("Underweight", "When the human body is too thin, the abdominal wall is loose and the abdominal muscles are weak, causing the muscles and ligaments that suspend and fix the position of the stomach to become loose and weak, and the abdominal pressure decreases. As a result, the physiological position of the entire stomach is lowered, and gastric peristalsis is weakened, thus triggering gastroptosis."),
            ("Obesity", "Obese people have an increased incidence of diabetes. Some studies show that 80%% of type 2 diabetes patients are obese, and the longer the obesity lasts, the higher the probability of getting diabetes. Obese people, especially those with abdominal obesity, due to factors such as consuming more fat, storing more body fat, hyperinsulinemia increasing blood lipids, and the clearance of blood lipids, are more likely to have dyslipidemia than ordinary people."),
            ("Obesity", "Obese people are prone to hypertension. Some obese people may experience blood pressure fluctuations. The incidence of hypertension in obese people aged 20 - 30 is twice that of those of the same age with normal weight. The incidence of hypertension in obese people aged 40 - 50 is 50%% higher than that of non - obese people. A moderately obese person (BMI > 30) has more than five times the risk of developing hypertension compared to a person with normal weight."),
            ("Obesity", "Obese people are prone to large - artery atherosclerosis, which is likely to rupture under the action of hypertension, causing cerebral hemorrhage and even endangering life. Secondly, obese people have a high level of tissue plasminogen activator inhibitor in their blood, making it difficult to dissolve blood clots and prone to cerebral infarction. Excessive lipid deposition in the coronary artery wall leads to lumen stenosis and hardening, making it easy to develop coronary heart disease and angina pectoris. At the same time, it increases the burden on the heart's pumping function, leading to heart failure."),
            ("Obesity", "Obesity causes thickening of the chest wall and abdominal fat, reducing lung capacity and vital capacity and affecting the normal ventilation function of the lungs. Due to insufficient ventilation, it may cause polycythemia and lead to vascular embolism. In severe cases, it may lead to pulmonary hypertension, cardiac enlargement, and congestive heart failure. Because of the accumulation of fat, it may also affect the activity of cilia in the trachea, preventing them from functioning properly."),
            ("Obesity", "Compared with normal people, the cholesterol content in the bile acid of obese people increases, exceeding the solubility in bile. Therefore, obese people are prone to a high proportion of gallstones. According to statistics, 30%% of obese people are found to have gallstones during surgery, while only 5%% of non - obese people do. Obese people often have fatty liver at the same time. According to statistics, the prevalence of fatty liver in obese people is as high as 50%, much higher than that in non - obese people."),
            ("Hypotension", "Hypotension refers to a blood pressure level lower than normal. Generally, an adult's upper - limb arterial blood pressure lower than 90/60 mmHg is considered hypotension. Primary hypotension, such as physiological hypotension, has an unclear cause and is related to a slender body shape and genetic factors. Secondary hypotension refers to a state of low blood pressure caused by certain diseases. One type is a rapid decrease in blood pressure in a short period, such as that caused by massive bleeding, dehydration, infection, and allergy. The other type is a slow and progressive decrease in blood pressure, which may be caused by heart diseases and endocrine diseases, including thyroid diseases, adrenal insufficiency, congenital heart diseases, and chronic heart failure. There are also postural hypotension, pregnancy - related hypotension, and post - meal hypotension."),
            ("Hypertension", "Hypertensive disease is a common chronic disease in life, seriously endangering physical health and quality of life. Hypertension itself can cause symptoms such as headache, dizziness, inattentiveness, and emotional instability. The damage of hypertension to the heart and blood vessels is mainly to the coronary arteries, while the other small arteries of the heart are rarely affected. Some studies suggest that due to increased blood pressure, the coronary arteries stretch, stimulating the proliferation of smooth muscle cells under the intima of the blood vessels, increasing elastin, collagen, and mucopolysaccharides in the arterial wall, damaging the intima and endothelial cells of the blood vessels, making it easier for cholesterol and low - density lipoproteins to penetrate the arterial wall, and causing fiber proliferation. In addition, due to an increase in lysosomes in smooth muscle cells, the elimination of cholesterol and other substances on the arterial wall is reduced."),
            ("Hypertension", "If blood pressure is elevated for a long time, it may lead to an increase in urine protein, chronic renal insufficiency, arteriosclerosis of the fundus retina, and further may induce diseases such as fundus hemorrhage, thus causing damage to target organs such as the fundus, brain, heart, and kidneys. In severe cases, it can lead to acute complications such as myocardial infarction, cerebral hemorrhage, stroke, and acute renal failure, directly endangering life."),
            ("Hypertension", "The children with a family history have twice the risk of developing hypertension compared to those without a family history. Patients with a family history have a lower age of onset and a higher blood pressure level compared to those without a family history. The incidence of hypertension increases with age, and the prevalence of hypertension in the elderly is generally high. Heavy smoking, drinking strong tea or coffee can also cause an increase in blood pressure because substances such as nicotine, theophylline, and caffeine can stimulate the sympathetic nervous system, increasing heart rate and blood pressure. Alcohol consumption also has a significant impact on blood pressure."),
            ("Tachycardia", "When the heart rate of an adult at rest exceeds 100 beats per minute (generally not exceeding 160 beats per minute), it is called sinus tachycardia. Tachycardia is divided into physiological and pathological types. The increase in heart rate during running, drinking alcohol, heavy physical labor, and emotional excitement is physiological tachycardia, which is commonly seen after excitement, agitation, smoking, drinking alcohol, drinking strong tea or coffee. If tachycardia is caused by diseases such as high fever, anemia, hyperthyroidism, bleeding, pain, hypoxia, heart failure, and cardiomyopathy, it is called pathological tachycardia, which is seen in pathological states such as infection, fever, shock, anemia, hypoxia, hyperthyroidism, and heart failure, or after taking drugs such as atropine, adrenaline, and ephedrine."),
            ("Bradycardia", "When the heart rate of an adult at rest is lower than 60 beats per minute (generally above 45 beats per minute), it is called sinus bradycardia. It can be seen in healthy people who engage in heavy physical labor for a long time and athletes. It can also be seen in cases of hypothyroidism, increased intracranial pressure, obstructive jaundice, and excessive use of drugs such as digitalis, quinidine, or propranolol. If the heart rate is lower than 40 beats per minute, sick sinus syndrome and atrioventricular block should be considered. If the pulse is uneven in strength, irregular, and the pulse rate is less than the heart rate, atrial fibrillation should be considered. If the heart rate exceeds 160 beats per minute or is lower than 40 beats per minute, it is mostly seen in patients with heart diseases. If accompanied by discomfort such as palpitations and chest tightness, a detailed examination should be carried out as soon as possible to treat the cause."),
            ("Bradycardia", "Many people have sinus bradycardia with arrhythmia, which is normal for most people and there is no need to worry too much. Sinus bradycardia refers to people with a heart rate lower than 60 beats per minute. Whether this symptom occurs is related to the frequency of bradycardia and the cause of bradycardia. At rest, the heart rate of adults between 50 - 60 beats per minute generally does not show obvious symptoms. Especially some well - trained athletes and people who engage in physical labor for a long time may not have obvious symptoms even if their heart rate is around 40 beats per minute at rest."),
            ("Bradycardia", "Physiologically, during normal sleep, due to increased vagus nerve tension, sinus bradycardia may occur, and the heart rate can be around 50 beats per minute, and occasionally around 40 beats per minute. Athletes may have a heart rate of around 50 beats per minute during the day, and at night, it may be as low as around 38 beats per minute. Manual laborers also often have sinus bradycardia. It can be seen in both young people and the elderly. Metabolic reduction (such as hypothermia, severe malnutrition, cachexia, hypopituitarism, hypothyroidism, etc.) and electrolyte disorders (such as hyperkalemia, uremia, or changes in blood pH) often also present with sinus bradycardia."),
            ("Bradycardia", "Peptic ulcer combined with sinus bradycardia. In the pathogenesis of peptic ulcer, the secretion of gastric acid is mainly controlled by the vagus nerve tension. When its excitability is increased, it can cause sinus bradycardia. Sinus bradycardia can also be caused by damage to the sino - atrial node function (such as inflammation, ischemia, poisoning, or degenerative damage). In addition, it can be seen in myocardial damage, such as myocarditis, pericarditis, endocarditis, cardiomyopathy, myocardial infarction, and myocardial sclerosis. It may also be caused by transient inflammation, ischemia, and toxic damage to the sino - atrial node. It has the highest incidence in the early stage of acute myocardial infarction, with an incidence of sinus bradycardia of 20%% - 40%%."),
            ("Hypolipidemia", "The main components of blood lipids are triglycerides and cholesterol, which are essential substances for the basic metabolism of living cells. Triglycerides are involved in the body's energy metabolism, while cholesterol is mainly used for the synthesis of cell plasma membranes, steroid hormones, and bile acids. Hypolipidemia refers to a low level of lipids in the blood, including total cholesterol, high - density lipoprotein, low - density lipoprotein, and triglyceride levels. It is commonly seen in diseases such as malnutrition, malabsorption syndrome, liver diseases, hyperthyroidism, chronic infections and other inflammations, hematological or other malignancies, and rare familial defects. Incorrect lifestyle factors such as an unreasonable diet, unbalanced nutrition intake, and excessive dieting can also lead to abnormal blood lipid levels."),
            ("Hyperlipidemia", "The main components of blood lipids are triglycerides and cholesterol, which are essential substances for the basic metabolism of living cells. Triglycerides are involved in the body's energy metabolism, while cholesterol is mainly used for the synthesis of cell plasma membranes, steroid hormones, and bile acids. To reliably reflect the true situation of blood lipid levels. Hyperlipidemia is a systemic metabolic disorder disease in which the levels of cholesterol, triglycerides, and low - density lipoproteins in the plasma are increased and the level of high - density lipoprotein is too low due to various reasons. The increase in cholesterol and triglyceride levels is related to the occurrence of atherosclerosis."),
            ("Hyperlipidemia", "Primary hyperlipidemia occurs when there is no other disease, generally due to genetic factors. Secondary hyperlipidemia is caused by other reasons, such as diabetes, hypothyroidism, nephrotic syndrome, kidney transplantation, biliary obstruction, etc. Bad eating habits such as overeating, alcoholism, picky eating, and irregular diet, as well as long - term mental stress leading to endocrine and metabolic disorders, can also lead to hyperlipidemia."),
        )
    else:
        lines = (
            ('吸烟','流行病学调查表明，吸烟是肺癌的重要致病因素之一，特别是鳞状上皮细胞癌和小细胞未分化癌。吸烟可降低自然杀伤细胞的活性，从而削弱机体对肿瘤细胞生长的监视、杀伤和清除功能。吸烟者喉癌发病率较不吸烟者高十几倍、膀胱癌发病率增加3倍。此外，吸烟与唇癌、舌癌、口腔癌、食道癌、胃癌、结肠癌、胰腺癌、肾癌和子宫颈癌的发生都有一定关系。临床研究和动物实验表明，烟雾中的致癌物质还能通过胎盘影响胎儿，致使其子代的癌症发病率显著增高。'),
            ('吸烟','吸烟是许多心、脑血管疾病的主要危险因素，吸烟者的冠心病、高血压病、脑血管病及周围血管病的发病率均明显升高。统计资料表明，冠心病和高血压病患者中75%有吸烟史。冠心病发病率吸烟者较不吸烟者高3.5倍，冠心病病死率前者较后者高6倍，心肌梗塞发病率前者较后者高2~6倍。吸烟者发生中风的危险是不吸烟者的2~3.5倍；如果吸烟和高血压同时存在，中风的危险性就会升高近20倍。此外，吸烟者易患闭塞性动脉硬化症和闭塞性血栓性动脉炎，吸烟可引起慢性阻塞性肺病，导致肺原性心脏病。'),
            ('吸烟','吸烟是慢性支气管炎、肺气肿和慢性气道阻塞的主要诱因之一。实验研究发现，长期吸烟可使支气管粘膜的纤毛受损、变短，影响纤毛的清除功能,吸烟者患慢性气管炎较不吸烟者高2～4倍，且与吸烟量和吸烟年限成正比例，患者往往有慢性咳嗽、咯痰和活动时呼吸困难。年轻的无症状的吸烟者也有轻度肺功能减退。吸烟导致的慢性阻塞性肺病易致自发性气胸。吸烟者常患有慢性咽炎和声带炎。'),
            ('吸烟','吸烟可引起胃酸分泌增加，比不吸烟者增加91.5%，并能抑制胰腺分泌碳酸氢钠，致使十二指肠酸负荷增加，诱发溃疡。烟草中烟碱可使幽门括约肌张力降低，使胆汁易于返流，从而削弱胃、十二指肠粘膜的防御因子，促使慢性炎症及溃疡发生，并使原有溃疡延迟愈合。此外，吸烟可降低食管下括约肌的张力，易造成返流性食管炎。烟草进入人体后，会干扰人体对钙离子的吸收就会受到影响，从而引起骨密度下降。'),
            ('饮酒','长期大量饮酒会导致心血管系统受损，饮酒之后产生多余的谷氨酸盐，会引起心脏的亢奋和血压升高，因此长期饮酒的人容易患高血压、心血管疾病，肾脏是人体的排毒器官之一，而酒精会损害肾脏和消化系统，当酒精进入肾脏之后，肾脏会直接将水送到膀胱而不能收回，导致身体缺水，而且大量的进入胃肠之后会刺激胃粘膜引起不适，严重的会导致胃溃疡和胃出血。'),
            ('饮酒','长期大量饮酒损害人的消化系统，酒精中含有大量的乙醇，而乙醇很容易被身体吸收，然后被肝脏分解，经常喝酒会给肝脏带来极大的负担，造成肝脏损害，很容易患上脂肪肝等其他疾病。大量的饮酒后会破坏身体的内分泌系统，会导致半乳糖赖量降低、甘油三酯合成增加，脂质过氧化增加，国际杂志BMC Public Health的研究报告中，来自瑞典于默奥大学的研究人员通过研究发现，从16岁开始，有规律的大量饮酒和酗酒或许和女性后期机体血液中较高的葡萄糖浓度直接相关，而血糖水平较高是2型糖尿病的一种风险因子。'),
            ('饮酒','长期大量饮酒会损害人的中枢神经系统，或导致人出现精神恍惚、倦怠无力、幻听、幻视、记忆减退、智力下降等，发表在《BMJ》杂志上的研究表明，即使中度的饮酒也会导致慢性的大脑认知水平的下降。'),
            ('糖尿病','糖尿病是一组以高血糖为特征的代谢性疾病。高血糖则是由于胰岛素分泌缺陷或其生物作用受损，或两者兼有引起。糖尿病时长期存在的高血糖，导致各种组织，特别是眼、肾、心脏、血管、神经的慢性损害、功能障碍。糖尿病存在明显的遗传异质性，具有家族发病倾向，1/4～1/2患者有糖尿病家族史。临床上至少有60种以上的遗传综合征可伴有糖尿病。'),
            ('体重消瘦','体重过轻的人常常会缺钙,而且因为脂肪量很少,很难练成肌肉,这样会影响骨细胞的功能和代谢,易致骨质疏松。过于消瘦者普遍存在营养摄入不均衡的问题,铁、叶酸、维生素B12等造血物质本身就摄入不足,进而发展为贫血。'),       
            ('体重消瘦','容易导致对病毒的抵抗力会下降，还容易出现疲劳的情况，产生摄入热量不足,消耗体内的脂肪供能,引起胆固醇移动,导致胆汁中胆固醇过高,胆汁变得黏稠,析出结晶并沉淀下来形成胆结石。'),       
            ('体重消瘦','当人体过分消瘦时,身体内腹壁松弛、腹肌薄弱,导致悬吊、固定胃位置的肌肉和韧带松弛无力,腹压下降,于是整个胃的生理位置就降低、胃蠕动减弱,从而引发胃下垂。'),
            ('体重肥胖','肥胖者会增加糖尿病患病发生率，有研究显示，在2型糖尿病中80%都是肥胖者，而且发生肥胖时间越长，患有糖尿病几率就越大。肥胖者特别是腹型肥胖者由于进食脂肪多、体内脂肪储存多、高胰岛素血症可增高血脂、血脂的清除等原因，所以，比普通人更容易表现为血脂紊乱。'),
            ('体重肥胖','肥胖者容易患高血压，有的肥胖人群会出现血压波动;20~30岁的肥胖者，高血压的发生率要比同年龄而正常体重者高1倍;40~50岁的肥胖者，高血压的发生几率要比非肥胖者高50%,一个中度肥胖(BMI>30)的人，发生高血压的几率是体重正常者的5倍多。'),
            ('体重肥胖','肥胖人群容易发生大动脉粥样硬化，易在高血压的作用下发生破裂，引起脑出血，甚至危及生命。其次，肥胖者血液中组织纤溶激活抑制因子较高，使血栓难以溶解,易发生脑梗死。而过多的脂质沉积在冠状动脉壁内，致使管腔狭窄、硬化，易发生冠心病、心绞痛，同时增加心脏泵血负担导致心功能衰竭。'),
            ('体重肥胖','肥胖造成胸壁与腹腔脂肪增厚，使肺容量下降、肺活量减少而影响肺部正常换气的功能。且因为换气不足，可能引起红血球增多症，造成血管栓塞。严重者可能发生肺性高血压、心脏扩大及梗塞性心衰竭。因为脂肪的堆积，亦可能影响气管内纤毛的活动，使其无法发挥正常功能。'),
            ('体重肥胖','肥胖者与正常人相比，胆汁酸中的胆固醇含量增多，超过了胆汁中的溶解度，因此肥胖者容易并发高比例的胆结石，据统计，30%的肥胖者手术发现有胆结石，而非肥胖者只占5%。肥胖者往往同时患有脂肪肝,据统计，肥胖者中脂肪肝患病率高达50%，远远高于非肥胖者发病率。'),
            ('低血压','低血压是指血压低于正常的水平。一般认为成年人上肢动脉血压低于90/60mmHg即为低血压。原发性低血压，比如生理性低血压，发病原因不清，与形体瘦弱、遗传因素有一定关联。继发性低血压是指某些疾病导致的低血压状态，一类为短期内迅速发生低血压，如大出血、脱水、感染、过敏等原因所致的血压急剧降低；另一类为缓慢发生逐渐加重，可能导致低血压的心脏病和内分泌疾病，包括甲状腺疾病、肾上腺功能不全、先天性心脏病、慢性心力衰竭等，还存在体位低血压、孕期低血压和餐后低血压等。'),
            ('高血压','高血压病是生活中常见慢性疾病,严重危害身体健康和生生活质量。高血压本身会引起头痛、眩晕、注意力不集中、情绪不稳定等症状。高血压对心脏血管的损害主要是冠状动脉血管，而心脏其他的细小动脉则很少度受累。有人研究认为，由于血压增高，冠状动脉血管伸张，刺激血管内层下平滑肌细胞增生，使动回脉壁弹力蛋白、胶原蛋白及粘多糖增多，血管内膜层和内皮细胞损伤，胆固醇和低密度脂蛋白易浸入动脉壁，以及纤维增生；另外，由于答平滑肌细胞内溶酶体增多，减少了对动脉壁上胆固醇等物质的消除。'),
            ('高血压','如果是长期的血压升高，有可能会导致尿蛋白升高，慢性肾功能不全，眼底视网膜动脉硬化，进一步有可能诱发眼底出血等疾病，从而造成眼底、大脑、心脏、肾脏等靶器官的损害,严重时会导致心肌梗死、脑出血、脑卒中、急性肾衰这类急性并发症，直接危害生命。'),
            ('高血压','有家族史的子女患高血压的危险是无家族史的2倍;有家族史患者较无家族史患者发病年龄偏低，血压水平较高。高血压随着年龄的增加而发病率上升，老年人高血压患病率普遍较高。大量吸烟、喝浓茶或浓咖啡等也可引起血压升高，这是因为尼古丁、茶碱、咖啡因这些物质能够兴奋交感神经系统，使心率加快、血压升高。饮酒对血压也有不小影响。'),
            ('心动过速','成人安静时心率超过100次/分钟（一般不超过160次/分钟），称为窦性心动过速，心动过速分生理性、病理性两种。跑步、饮酒、重体力劳动及情绪激动时心律加快为生理性心动过速，常见于兴奋、激动、吸烟、饮酒、喝浓茶或咖啡后；若高热、贫血、甲亢、出血、疼痛、缺氧、心衰和心肌病等疾病引起心动过速，称病理性心动过速，见于感染、发热、休克、贫血、缺氧、甲亢、心力衰竭等病理状态下，或见于应用阿托品、肾上腺素、麻黄素等药物后。'),
            ('心动过缓','成人安静时心率低于60次/分钟（一般在45次/分钟以上），称为窦性心动过缓，可见于长期从事重体力劳动的健康人和运动员；或见于甲状腺机能低下、颅内压增高、阻塞性黄疸以及洋地黄、奎尼丁或心得安类药物过量。如果心率低于40次/分钟，应考虑有病态窦房结综合征、房室传导阻滞等情况。如果脉搏强弱不等、不齐且脉率少于心率，应考虑心房纤颤。心率超过160次/分钟，或低于40次/分钟，大多见于心脏病患者，如常伴有心悸、胸闷等不适感，应及早进行详细检查，以便针对病因进行治疗。'),
            ('心动过缓','很多人都会有窦性心动过缓伴不齐，对于多数人来说是正常的，不必过于担心。窦性心动过缓是指心率低于60次/分钟的人，是否会出现此症状，与其心跳过缓的频率和引起心跳过缓的原因有关。在安静状态下，成年人的心率若在50～60次/分钟之间一般不会出现明显症状。尤其是一些训练有素的运动员以及长期从事体力劳动的人，在安静状态下即使其心率在40次/分钟左右也不会出现明显症状。'),
            ('心动过缓','生理性在正常睡眠时，由于迷走神经张力增高可出现窦性心动过缓，心率可在50次/分钟左右，个别可在40次/分钟左右。运动员白昼可在50次/分钟左右，夜间个别可低至38次/分钟左右。体力劳动者也常出现窦性心动过缓。可见于年轻人及老年人。代谢降低(如低温、重度营养不良恶病质、脑垂体功能低下、甲状腺功能减低症等)、电解质紊乱(如高钾血症、尿毒症或血液酸碱度改变者)也常出现窦性心动过缓。'),
            ('心动过缓','消化性溃疡合并窦性心动过缓，消化性溃疡在发病机制中，胃酸的分泌物主要受迷走神经张力控制，当其兴奋性增高时可引起窦性心动过缓。窦房结功能受损（如炎症、缺血、中毒或退行性变的损害等）而引起的窦性心动过缓。此外，可见于心肌受损，如心肌炎、心包炎、心内膜炎、心肌病、心肌梗死、心肌硬化等。也可能为一过性的窦房结炎症、缺血及中毒性损害所致。在急性心肌梗死发病早期发生率最高,窦性心动过缓的发生率为20%～40%。'),
            ('低脂血','血脂中的主要成分是甘油三酯和胆固醇，它们是生命细胞的基础代谢必需物质。其中甘油三酯参与人体内能量代谢，而胆固醇则主要用于合成细胞浆膜、类固醇激素和胆汁酸。低脂血症是指血液中脂类含量较低，包括总胆固醇含量，高密度脂蛋白，低密度脂蛋白以及甘油三酯的含量。常见于营养不良、吸收不良综合征、肝脏疾病、甲状腺功能亢进症、慢性感染与其他炎症、血液系统或其他恶性肿瘤、罕见的家族性缺陷等疾病，饮食不合理、营养摄入不均衡、过度节食导致等不正确的生活方式，也会会导致血脂异常。'),
            ('高脂血','血脂中的主要成分是甘油三酯和胆固醇，它们是生命细胞的基础代谢必需物质。其中甘油三酯参与人体内能量代谢，而胆固醇则主要用于合成细胞浆膜、类固醇激素和胆汁酸。为可靠地反映血脂水平的真实情况。高脂血症是由各种原因导致的血浆中的胆固醇、甘油三酯以及低密度脂蛋白水平升高和高密度脂蛋白过低的一种的全身质代谢异常疾病，胆固醇和甘油三酯水平的升高与动脉粥样硬化的发生有关。'),
            ('高脂血','原发性高脂血症是原来无任何其他疾病而发生高脂血症，一般是因为遗传因素。而继发性高脂血症是由于其它原因引起的高脂血症，比如：糖尿病、甲状腺功能减退、肾病综合征、肾移植、胆道阻塞等。暴饮暴食、嗜酒、偏食、饮食不规律等不良饮食习惯和长期精神紧张、导致内分泌代谢紊乱，也会导致的高脂血症；'),
        )
    for line in lines:
        print(line[0])
        hmtype=Indicator.objects.filter(name=line[0]).first()

        if hmtype:
            print(type(hmtype),line[0],line[1])
            RiskAnalyse.objects.get_or_create(hmtype = hmtype,risk =line[1])
    if settings.LANGUAGE_CODE == 'en':
        intervents = (
            ("Smoking", "Smoking is highly harmful to the human body. Quitting smoking is the only way to reduce the harm of smoking. The earlier one quits, the better. Quitting at any age can bring benefits. Therefore, it is recommended to gradually reduce the number of cigarettes smoked in a step - by - step manner. If it is really impossible to quit completely, it is advisable to reduce the amount of smoking or use tobacco substitutes."),
            ("Smoking", "Smokers are advised to supplement vitamins. Certain compounds in cigarette smoke can greatly reduce the activity of vitamins A, B, C, E, etc., and cause a large consumption of these vitamins in the body. Therefore, smokers should often eat more foods rich in vitamins, such as milk, carrots, peanuts, cornmeal, bean sprouts, Chinese cabbage, vegetable oil, etc. This can not only supplement the vitamin deficiency caused by smoking but also enhance the body's immune function."),
            ("Smoking", "Smokers are advised to drink more tea regularly. Because the compounds contained in cigarette smoke can lead to thickening of the arterial intima, a significant reduction in gastric acid secretion, and an increase in blood sugar, etc. The unique catechins in tea can effectively prevent cholesterol from depositing on the blood vessel wall, increase gastrointestinal peristalsis, and reduce blood and urine sugar. Smokers should often drink more tea to reduce the occurrence of these diseases caused by smoking. At the same time, tea can promote diuresis and detoxification, and some toxic substances in cigarettes can be excreted with urine, reducing their residence time in the body."),
            ("Smoking", "Frequent smoking can easily lead to a low content of selenium in human blood, and selenium is an essential trace element for preventing and combating cancer. Therefore, smokers should often eat more foods rich in selenium, such as animal livers, seaweeds, and shrimps. They can also appropriately supplement foods rich in iron, such as animal livers, meat, kelp, and beans. Foods rich in vitamin E, such as nuts and coarse grains, can reduce the incidence of lung cancer in smokers by about 20%."),
            ("Smoking", "Because smoking increases the deposition of cholesterol and fat in blood vessels, reduces blood supply to the brain, and is likely to cause brain atrophy and accelerate brain aging. Therefore, one should eat fatty meat containing saturated fatty acids and increase foods that can reduce or inhibit cholesterol synthesis, such as milk, fish, soy products, and high - fiber foods. Alkaline foods rich in β - carotene can effectively suppress the urge to smoke and play a certain role in reducing the amount of smoking and quitting smoking, such as carrots, spinach, pea sprouts, alfalfa, and peppers."),
            ("Drinking", "When drinking alcohol, one must eat some food first and then drink, and drink in small amounts and slowly to avoid getting drunk. Each time when drinking, one must drink plenty of water to avoid dehydration of body cells. After sobering up, replenish some water. Alcohol consumers should have a balanced diet in daily life and appropriately supplement complex vitamins B1 and B3, etc., such as oats, whole - wheat bread, animal offal, lean meat, peanuts, vegetables, wheat bran, milk, etc. Eat honey and fruit juice regularly, and avoid fried and fatty foods. Long - term heavy drinking or alcoholism is very harmful to the human body. Therefore, it is recommended to quit drinking or control the amount of alcohol consumed and strengthen physical exercise."),
            ("Underweight", "Exclude the potential impacts of diseases such as thyroid, diabetes, adrenal, and digestive system diseases. On this basis, achieve scientific weight gain by maintaining a normal and regular diet, ensuring an appropriate intake of carbohydrates, supplementing sufficient protein, mainly consuming grains, supplemented by eggs and milk, and eating more fruits. Strengthen physical exercise and maintain sufficient and good sleep."),
            ("Obesity", "Change eating behavior, increase the number of chewing times, slow down the eating speed, and drink a bowl of soup before meals. This can not only help the secretion of digestive juices but also increase satiety and reduce food intake. Limit the total energy intake, mainly by reducing the intake of cereal staple foods. The intake should be lower than the consumption, so that the weight gradually decreases. Adopt a diet high in protein, low in fat, low in sugar, high in vitamins, and low in salt. For example, eat more high - protein foods such as eggs, milk, beef, fish, shrimp, chicken, soybeans, and peanuts. Limit high - fat foods such as fatty meat, animal offal, and fried foods. Eat less high - calorie foods such as desserts, candies, and chocolates. Eat more vegetables, whole grains, and an appropriate amount of fruits, that is, the daily intake of sodium salt is less than 5 grams."),
            ("Obesity", "Insist on physical labor or physical exercise, choose suitable sports events and appropriate exercise intensity. The best exercise time is from 3:00 pm to 5:00 pm every day. For example, if you exercise before meals, wait for 30 minutes before eating; exercise 1.5 hours after meals. You can adjust the exercise intensity according to your own situation. The exercise intensity is measured by the number of pulse beats per minute. For people aged 30 - 40, it should not exceed 130 beats, for those aged 40 - 50, it should not exceed 120 beats, and for those over 60, it should not exceed 110 beats. And it should be carried out step by step according to personal circumstances, limited by the physiological tolerance. In the first two months of starting exercise, the weight loss is not obvious, but if you persist for more than two months, the effect will gradually become obvious."),
            ("Obesity", "The key to reasonable nutrition lies in “moderation”, which is mainly achieved through a balanced diet. A balanced diet means that the nutrients contained in the diet are complete in variety, sufficient in quantity, and appropriate in proportion. The diet should be diverse with grains as the mainstay. A balanced diet must consist of a variety of foods, and it is advocated to eat a wide range of foods. A variety of foods include five categories: grains and tubers; animal foods; beans and their products; vegetables and fruits; pure energy foods."),
            ("Obesity", "Control the amount of food. You can't over - eat vegetables, fruits, and tubers. Eating too much of a diet rich in vegetables, fruits, and tubers can also lead to weight gain. Often eat beans and their products, which are rich in protein and vitamins, have a high calcium content, and a high utilization rate. Often eat an appropriate amount of fish, poultry, eggs, and lean meat, and eat less fatty meat and animal fat."),
            ("Obesity", "For people with grade I obesity, it is advisable to lose 0.5 - 1 kg of weight per week. They should control their food intake and eat low - fat, low - cholesterol, and low - salt foods. For people with grade II and grade III obesity, in addition to strictly controlling their diet like those with grade I obesity, they should use weight - loss drugs or starvation therapy under the guidance of a doctor."),
            ("Obesity", "Due to fear of heat, excessive sweating, low resistance, and easy wear and tear in the purple lines and folds of the skin, obese people are prone to infections, causing dermatitis, tinea, etc. They should take baths frequently, change clothes frequently, and keep the skin dry and clean."),
            ("Obesity", "Before treatment, obese patients should go to the hospital for a series of examinations to rule out other endocrine and metabolic diseases. During the treatment period, they should measure their weight 1 - 2 times a day. Weight - loss drugs should be used with caution, preferably under the guidance of a doctor."),
            ("Diabetes", "At present, there is no radical cure for diabetes. However, through scientific and reasonable treatment methods, most diabetes patients can have the same quality of life and lifespan as non - diabetes patients. The five key points of comprehensive diabetes management (also known as the “five - in - one approach”) include: diabetes education, medical nutrition therapy, exercise therapy, drug therapy, and blood glucose monitoring."),
            ("Diabetes", "Diabetes education: Patients and their families should learn as much as possible about diabetes and its complications, actively seek help from professionals, follow medical advice for treatment, and improve their self - management awareness and ability."),
            ("Diabetes", "Medical nutrition therapy: Medical nutrition therapy is a basic management measure for diabetes. It aims to help patients develop a nutrition plan, form good eating habits, determine a reasonable total energy intake, rationally and evenly distribute various nutrients, and restore and maintain an ideal weight. Generally, the ideal weight can be estimated by height (cm) - 105. For adult patients with normal weight, 15 - 20 kcal of energy is required per kilogram of ideal weight per day when completely bedridden, and 25 - 30 kcal under a resting state. The energy intake can be increased as appropriate according to the physical labor situation."),
            ("Diabetes", "The dietary nutrition distribution should be balanced. Carbohydrates should account for 50 - 60% of the total calories. The daily staple food intake for adult patients is 250 - 400 g, and the intake of simple sugars and disaccharides should be restricted. Protein intake accounts for 15 - 20% of the total calories. Adult patients are given 0.8 - 1.2 g of protein per kilogram of ideal weight per day, and at least half of the protein should come from animal proteins. The daily fat intake accounts for 25 - 30% of the total calories, of which the saturated fatty acid intake is less than 10% of the total energy, and the cholesterol intake is less than 300 mg/d. Foods rich in dietary fiber are recommended. The daily intake of energy should be reasonably distributed among meals, which can be distributed as 1/5, 2/5, 2/5 or 1/3, 1/3, 1/3 for three meals a day."),
            ("Diabetes", "Exercise therapy: Exercise therapy is particularly important for type 2 diabetes patients with obesity. It should be carried out under the guidance of a doctor, and it is recommended to have 150 minutes of moderate - intensity exercise per week."),
            ("Diabetes", "Blood glucose monitoring: Condition monitoring mainly based on blood glucose monitoring is also very important. The blood glucose monitoring indicators mainly include fasting and post - meal blood glucose and glycosylated hemoglobin. Glycated albumin can be used to evaluate the short - term efficacy after adjusting the blood glucose control plan. Patients can use a portable blood glucose meter for self - blood glucose monitoring at home. In addition, condition monitoring should also include the monitoring of cardiovascular risk factors and complications. Patients should have a blood lipid test at least once a year, as well as comprehensive examinations of the heart, kidneys, nerves, fundus, etc."),
            ("Diabetes", "Drug therapy: Currently, diabetes treatment drugs include two major categories: oral medications and injection preparations. Oral hypoglycemic drugs mainly include insulin secretagogues, non - insulin secretagogues, dipeptidyl peptidase - 4 inhibitors, and sodium - glucose co - transporter 2 inhibitors. Injection preparations include insulin and insulin analogs, and glucagon - like peptide - 1 receptor agonists."),
            ("Hypotension", "Many cases of hypotension, like hypertension, cannot be completely cured. However, through adjustments to the patient's lifestyle, such as eating habits, exercise methods, and medication, its occurrence can be effectively prevented and controlled. In daily life, avoid bending over at the waist and getting up directly. If symptoms of hypotension occur, squeezing the muscles of the thighs, abdomen, and buttocks can relieve related symptoms. Pay attention to environmental changes and try to reduce the impact of climate and environmental changes on blood pressure. For example, add clothes in autumn and winter in a timely manner and avoid too low room temperature. Avoid using overly hot bath water or taking too long a bath, as this can dilate blood vessels and lower blood pressure. For severe postural hypotension caused by spinal cord injury or autonomic nervous system failure, use an abdominal belt or elastic bandage to briefly pressurize the abdomen or lower limbs before standing."),
            ("Hypotension", "Develop healthy eating habits, ensure a balanced diet, and ensure all the nutrients required for health. Consume an appropriate amount of salt according to medical advice, which can relieve symptoms of hypotension. Reduce the intake of carbohydrates. To prevent a sharp drop in blood pressure after meals, it is recommended to eat small and frequent meals every day and limit high - carbohydrate foods such as potatoes, rice, noodles, and bread. Strengthen nutrition, eat more easily digestible foods rich in protein, such as eggs, fish, cheese, and milk, drink more soups and water, appropriately increase the intake of salt, and at the same time pay attention to supplementing iron and vitamins to prevent anemia."),
            ("Hypotension", "Appropriately strengthen exercise and maintain a good mental state to improve the regulatory function of blood vessels, accelerate blood circulation, and avoid low blood pressure. Drink less alcohol, as alcohol can cause dehydration, and even moderate alcohol consumption can lower blood pressure. Drink more water, as water can increase blood volume and thus raise blood pressure. When sleeping at night, raise the head of the bed, which can relieve symptoms of hypotension. Sit up a few minutes after waking up, sit by the bed for 1 - 3 minutes, and gradually transition to a standing position, which helps to promote the return of venous blood to the heart and reduce the occurrence of postural hypotension. Try to reduce the time spent in bed for a long time."),
            ("Hypertension", "Cultivate correct eating habits. In daily life, the intake of sodium salt should be reduced, and a light diet should be adopted. Reduce high - sodium foods such as soy sauce, pickled products, and carbonated beverages with a high sodium content. The Chinese Dietary Guidelines recommend that the daily salt intake for adults should not exceed 6 grams. In addition, eating more potassium - rich foods can increase the excretion of sodium, improve the blood vessel environment, and enhance blood vessel elasticity. Appropriately increase the intake of vegetables such as soybeans, tomatoes, celery, and edible mushrooms, as well as fresh fruits such as oranges, apples, bananas, kiwis, pineapples, and walnuts to supplement potassium ions in the body."),
            ("Hypertension", "Keep a calm mood and avoid emotional excitement, excessive tension, and anxiety. Avoid long - term over - intense work and fatigue, ensure sufficient sleep, combine work and rest, and choose suitable exercise and relaxation therapies such as walking and Taijiquan. The exercise intensity should not be too high. A commonly used exercise intensity index is that the maximum heart rate during exercise reaches 170 minus the age, and it is appropriate to return to normal after 15 - 30 minutes of rest. Avoid taking a bath with overly hot water or taking a long steam bath. Persist in long - term medication, do not stop taking the medicine without permission, do not arbitrarily increase or decrease the dosage, understand the effects and side effects of the medicine. When standing up from a sitting position or sitting up from a lying position, move as slowly as possible to avoid fainting. Report any abnormalities to the doctor in a timely manner and adjust the medication."),
            ("Bradycardia", "By participating in various exercises with appropriate intensity, the heart function can be exercised, and the resting heart rate can gradually return to normal. Generally, the appropriate exercise heart rate is “170 - age”. For example, for a 50 - year - old person, the exercise heart rate should be controlled at 120 beats per minute. If it is too fast, it means the exercise intensity is too high, and if it is not reached, it will not have an effect. Before exercise, one should feel comfortable and not fatigued. Generally, the exercise should not exceed 1 hour, and the best time for each exercise is 30 - 60 minutes. One should adhere to exercise at least 3 times a week."),
            ("Bradycardia", "Correct bad lifestyle habits. Staying up late, smoking, drinking alcohol, and drinking less strong tea, especially not before going to bed, otherwise it is easy to cause insomnia. Maintain an appropriate weight. Being too thin and malnourished cannot provide the energy required by the heart. Therefore, those who are too thin and malnourished should maintain an appropriate weight through fitness exercises and dietary adjustments."),
            ("Bradycardia", "In case of an acute episode of bradycardia, in addition to treating the primary cause and stopping drugs that can slow down the heart rate, atropine and isoprenaline can be used to increase the heart rate. For those with a heart rate of 40 beats per minute or slower, the effect of drugs to increase the heart rate is not obvious, especially for patients with repeated syncope or pre - syncope symptoms. A pacemaker should be implanted."),
            ("Tachycardia", "An increased heart rate is harmful to health, shortens lifespan, and increases the incidence and mortality of cardiovascular diseases. Regular participation in various exercises with appropriate intensity can slow down the resting heart rate. Although the heart rate increases during exercise, exercise can improve heart function, thus reducing the resting heart rate. Generally, the appropriate exercise heart rate is calculated as '170 - age'. For example, for a 50 - year - old person, the exercise heart rate should be controlled at around 120 beats per minute. If it is too fast, it indicates that the exercise intensity is too high, and if it fails to reach this rate, the exercise may not be effective. Before exercising, one should feel comfortable and not fatigued. Generally, the exercise duration should not exceed 1 hour, with the optimal time for each session being 30 to 60 minutes. It is recommended to exercise at least 3 times a week."),
            ("Tachycardia", "Correct unhealthy lifestyle habits. Staying up late, smoking, and drinking alcohol can all increase the resting heart rate. Drink less strong tea, especially avoid drinking it before bedtime, as it can easily lead to insomnia. Also, maintain regular bowel movements to ensure smooth defecation. Keep an appropriate weight, as obesity can 加重心脏负担 and accelerate the heart rate. Therefore, obese individuals should engage in fitness exercises and adjust their diet to maintain a suitable weight. Keep a calm state of mind, avoid getting anxious or angry. When the heart rate is too fast, one can gradually calm down by listening to music, meditating, etc."),
            ("Tachycardia", "For the increased heart rate caused by certain diseases such as hypertension and coronary heart disease, medications can be taken as prescribed by a doctor. Drugs like propafenone and verapamil can terminate the attacks of some types of tachycardia, but they cannot provide a radical cure. Injecting these drugs carries certain risks, and long - term use to prevent the recurrence of tachycardia is not recommended. Radiofrequency ablation can completely cure tachycardia. After the operation, there is no need to use anti - arrhythmia drugs anymore. The patient experiences no pain, and the operation method is simple. It is characterized by minimal trauma, quick recovery, and a high cure rate."),
            ("Hypolipidemia", "On the basis of ruling out primary diseases, it is recommended to improve eating habits, have a balanced diet with a proper combination of meat and vegetables. Eat more high - cholesterol foods such as poultry eggs, seafood, and animal livers appropriately. Increase exercise in moderation and regularly review changes in blood lipid levels. If there is no change, a comprehensive physical examination is recommended."),
            ("Hyperlipidemia", "On the basis of ruling out primary diseases, patients with hyperlipidemia need to pay attention to their daily diet and exercise to reduce the risk of cardiovascular and cerebrovascular diseases and other related diseases. It is recommended to control the diet, reduce the intake of saturated fatty acids (vegetable oil, fish oil) and cholesterol, with a daily intake of less than 300mg. Reduce the daily fat intake (less than 30g of cooking oil), increase dietary fiber, supplement plant sterols and soluble fiber, limit salt intake, quit smoking, limit alcohol consumption, and avoid drinking strong liquor."),
            ("Hyperlipidemia", "Strengthen physical exercise by engaging in moderate - intensity physical activities for 30 minutes, 5 to 7 days a week. People with cardiovascular and cerebrovascular diseases, risk factors for cardiovascular diseases, hypertension, diabetes, smokers, excessive drinkers, obese individuals, those with a family history of early - onset cardiovascular diseases, those with familial hyperlipidemia, and those with xanthomas on the skin or tendons are advised to regularly monitor their blood lipid levels. Under normal circumstances of non - drug treatment, the blood lipid levels should be re - examined every 3 to 6 months. If the blood lipid levels are up to standard, the re - examination interval can be extended to every 6 to 12 months. For those undergoing lipid - regulating drug treatment, the blood lipid levels, liver function, and creatine kinase levels should be re - examined within 6 weeks. If the blood lipid levels are up to standard, the re - examination interval can be extended to every 6 to 12 months. If the blood lipid levels are not up to standard, re - examine again after 3 months. If it still fails to meet the standard, adjust the treatment plan.")    
        )
    else:
        intervents = (
            ('吸烟','吸烟对人体的危害较大，戒烟是降低吸烟危害的唯一方法，戒烟越早越好，任何年龄戒烟均可获益，因此建议采用逐渐减少吸烟次数的方法，循序渐进的进行戒烟，如实在无法戒除建议减少吸烟量，或通过使用烟草替代品。'),
            ('吸烟','吸烟者建议补充维生素。烟气中的某些化合物，可使维生素a、b、c、e等的活性大为降低，并使体内的这些维生素得到大量消耗。因此，吸烟者宜经常多吃富含维生素的食物，如牛奶、胡萝卜、花生、玉米面、豆芽、白菜、植物油等。这样既可补充由于吸烟所引起的维生素缺乏，又可增强人体的自身免疫功能。'),
            ('吸烟','吸烟者建议经常多喝茶。因烟气中含有的化合物可导致动脉内膜增厚，胃酸分泌量显著减少及血糖增高等症，而茶叶中所特有的儿茶素等可有效防止胆固醇在血管壁沉积，增加胃肠蠕动及降低血、尿糖等。吸烟者宜经常多喝茶，以降低吸烟所带来的这些病症的发作。同时，茶能利尿、解毒，还可使烟中的一些有毒物随尿液排出，减少在体内停留时间。'),
            ('吸烟','经常吸烟易导致人体血液中硒元素含量偏低，而硒又是防癌抗癌所不可缺少的一种微量元素。因此，吸烟者应经常多吃一些含硒丰富的食物，如动物肝脏、海藻及虾类等。可适当补充含铁的食物，如动物肝脏、肉、海带、豆类。坚果和粗粮等含维生素e的食物可使吸烟者得肺癌的发病率降低约20%。'),
            ('吸烟','因吸烟使血管中的胆固醇及脂肪沉积量加大，大脑供血量减少，易致脑萎缩，加速大脑老化等。因此，应吃含饱和脂肪酸的肥肉等，增加降低或抑制胆固醇合成的食物，如牛奶、鱼类、豆制品及高纤维食物，富含β-胡萝卜素的碱性食物能有效抑制烟瘾，对减少吸烟量和戒烟都有一定作用。如胡萝卜、菠菜、豌豆苗、苜蓿、辣椒等。'),
            ('饮酒','饮酒时一定要先吃一部分食物后再喝酒，同时做到少量及慢慢喝，避免醉酒，每次喝酒时，一定要多饮水，避免体内细胞脱水，酒醒后再补充部分水，饮酒者日常应饮食均衡，适当补充复合维生素B1、B3等，如燕麦、全麦面包、动物内脏、瘦肉、花生、蔬菜、麦麸、牛奶等，常吃蜂蜜，果汁，不要吃油炸及脂肪食物。长期大量饮酒或酗酒对人体的危害较大，因此建议戒酒或控制饮酒量，加强体育锻炼。'),
            ('体重消瘦','排除如甲状腺、糖尿病、肾上腺、消化系统疾病等疾病的潜在影响，在此基础上做到科学增重，保持正常和规律的饮食，保证碳水化合物的摄入量，补充充足的蛋白质，以谷物为主,蛋、奶为辅,多吃水果。加强体育锻炼，保持充足而良好的睡眠。'),            
            ('体重肥胖','改变进食行为，增加咀嚼次数，减慢进食速度，饭前先喝一碗汤，既帮助消化液的分泌，又增加饱腹感，减少饮食量。限制总热能摄入量，以减少谷类主食摄入量为主。摄入量应低于消耗量，以使体重逐渐下降。采用高蛋白、低脂肪、低糖、高维生素、低盐饮食。如：多食用鸡蛋、牛奶、牛肉、鱼、虾、鸡、大豆、花生等高蛋白食物，限制高脂肪食物，如肥肉、动物内脏、油炸食品等，少食高热量的食物，如甜食、糖果、巧克力等，多食蔬菜、杂粮，食用适量水果，即每天摄入的钠盐少于5克。'),
            ('体重肥胖','坚持体力劳动或体育锻炼，选择适宜的运动项目和适宜的运动量，最佳运动时间为每天的15：00—17：00。如在饭前锻炼后间隔30min吃饭；饭后1.5h锻炼。可根据自身情况掌握运动强度。运动强度以每分钟脉搏次数为尺度，30-40岁不超过130次，40-50岁不超过120次，60岁以上不超过110次，并要根据个人情况循序渐进，以生理耐受量为限。开始运动的头两个月，体重下降不明显，但如坚持2个月以上疗效渐明显。'),
            ('体重肥胖','合理营养的关键在于“适度”，主要在通过平衡膳食来实现。平衡膳食是指膳食中所含营养素，种类齐全、数量充足、比例适当。食物多样、谷物为主,平衡膳食必须由多种食物组成，提倡广泛食用多种食物。多种食物包括五大类：谷类及薯类；动物性食物；豆类及其制品；蔬菜及水果类；纯热能食物。'),
            ('体重肥胖','控制食物量，不能多吃蔬菜、水果和薯类，含丰富蔬菜、水果和薯类的膳食吃多了，同样发胖。常吃豆类及其制品，含有丰富的蛋白质和维生素，含钙量较高，利用率高。经常吃适量的鱼、禽、蛋、瘦肉，少吃肥肉和荤油'),
            ('体重肥胖','I度肥胖者：体重以每周减轻0.5-1公斤为宜，应控制食量，进食低脂、低胆固醇、低盐食物；II度和III度肥胖者：除与I度肥胖者一样严格控制饮食外，在医生指导下使用减肥药物或饥饿疗法。'),
            ('体重肥胖','肥胖症由于怕热多汗，抵抗力低，皮肤紫纹及皱折处易磨损，易感染，引起皮炎、皮癣等，应勤洗澡，勤更衣，保持皮肤干燥清洁。'),
            ('体重肥胖', '肥胖患者在治疗前应到医院做一系列检查以排除有无其它内分泌代谢疾病，治疗期间应每天测体重1-2次。应慎重应用减肥药物，最好在医生指导下用药。'),
            ('糖尿病','目前尚无根治糖尿病的方法，但可以通过科学合理的治疗方法，使大多数糖尿病患者具有与非糖尿病者同等的生活质量和寿命。糖尿病综合管理的5个要点(又称五驾马车)包括：糖尿病教育、医学营养治疗、运动治疗、药物治疗、血糖监测。'),
            ('糖尿病','糖尿病教育：患者及家属应尽可能多的学习、了解糖尿病及其并发症相关知识，积极向专业人士寻求帮助，谨遵医嘱进行治疗，提高自我管理的意识及能力。'),
            ('糖尿病','医学营养治疗：医学营养治疗是糖尿病的基础管理措施，旨在帮助患者制定营养计划，形成良好的饮食习惯，确定合理的总能量摄入，合理均衡分配各种营养物质，恢复并维持理想体重。一般可根据身高（cm）-105估计理想体重。成人正常体重者完全卧床时每日每千克理想体重需要给予能量15~20kal，休息状态下25~30kcal ，根据体力劳动情况酌情增加能量摄入。'),
            ('糖尿病','膳食营养分配要均衡，碳水化合物供给量占总热量50~60%，成年患者每日主食摄入量为250~400g，限制单糖和双糖摄入。蛋白摄入量占总热量15~20%，成年患者每日每千克理想体重给予0.8~1.2g，至少半数蛋白应来自动物蛋白质。每日脂肪摄入量占总热量25~30%，其中饱和脂肪酸摄入量低于总能量的10%，胆固醇摄入量低于300mg/d。推荐富含膳食纤维的食品。每日摄入能量应合理分配于各餐次，可按照每日三餐1/5、2/5、2/5或1/3、1/3、1/3分配。'),
            ('糖尿病','运动治疗：运动治疗对于伴肥胖的2型糖尿病患者尤为重要，应在医师指导下进行，建议每周150min的中等强度运动。'),
            ('糖尿病','血糖监测：以血糖监测为主的病情监测亦非常重要。血糖监测指标主要是空腹和餐后血糖及糖化血红蛋白。糖化白蛋白可用于评价血糖控制方案调整后短期的疗效。患者可以使用便携式血糖仪在家中进行自我血糖监测。此外，病情监测还应包括心血管危险因素和并发症的监测，患者每年至少要进行一次血脂检查以及全面的心、肾、神经、眼底等相关检查。'),
            ('糖尿病','药物治疗：目前糖尿病治疗药物包括口服药和注射制剂两大类。口服降糖药主要有促胰岛素分泌剂、非促胰岛素分泌剂、二肽基肽酶-4抑制剂和钠-葡萄糖共转运蛋白2抑制剂。注射制剂有胰岛素及胰岛素类似物、胰高血糖素样多肽-1受体激动剂。'),
            ('低血压','很多低血压像高血压一样无法彻底根治，但通过对患者生活方式的调整，如饮食习惯、运动方式、用药等，可以有效地预防和控制其发生。日常应避免腰部弯曲、避免直接起身，如果出现低血压症状，挤压大腿、腹部和臀部肌肉能缓解相关症状。注意环境变化，需尽量减少气候和环境改变对血压的影响，例如秋冬季及时增加衣物、避免室温过低等。避免洗澡水过热或洗澡时间过长，使血管扩张而降低血压。对于脊髓损伤或自主神经功能衰竭所致的严重体位性低血压，站立之前使用腹带或弹力绷带对腹部或下肢短时加压。'),
            ('低血压','养成健康饮食的习惯，保证营养均衡，确保健康所需的所有营养。根据医嘱食用适量的盐，可缓解低血压症状。减少碳水化合物的摄入，为了防止餐后血压急剧下降，建议每天少食多餐，并限制高碳水化合物的食物，如土豆、大米、面条和面包等。加强营养，多食易消化富含蛋白质的食物，如鸡蛋、鱼、奶酪、牛奶等，多喝汤多饮水，适当增加盐分的摄入，同时注意补充铁剂和维生素，防止贫血。'),
            ('低血压','适当加强锻炼，保持良好的精神状态，以便改善血管的调节功能，加速血液循环，避免血压偏低。少喝酒，酒精会使人脱水，即使适度饮酒，也能降低血压；多喝水，水可以可增加血容量，从而升高血压。晚上睡觉时将头部垫高，可减轻低血压的症状。睡醒后几分钟再坐起，在床边坐1~3分钟，逐渐过渡到站立位，有助于促进静脉血向心脏回流，减少体位性低血压的发生，尽可能减少长时间卧床。'),
            ('高血压','培养正确的饮食习惯，日常生活中应该减少钠盐的摄入，以清淡饮食为主。减少高钠食品如酱油、腌制品、碳酸饮料等含钠量高的食物，中国膳食指南建议，成人每天食盐量不应超过6克。此外，多食富含钾的食物可以增加钠的排出，改善血管环境，增强血管弹性。适当增加黄豆、番茄、芹菜、食用菌等蔬菜以及橘子、苹果、香蕉、猕猴桃、菠萝、核桃、等新鲜水果的摄入量，以补充身体内的钾离子。'),
            ('高血压','保持平静心情，避免情绪激动及过度紧张焦虑。避免长期过度紧张工作和劳累，保证充足睡眠，劳逸结合，选择合适的运动锻炼和放松疗法如步行、太极拳等。运动量不宜太大，常用运动强度指标为运动时最大心率达到170减去年龄，且休息15—30分钟后恢复正常为宜。避免使用过热的水洗澡或长时间蒸汽浴。坚持长期用药，不擅自停药，不随意增减剂量，了解药物作用与副作用，坐位起立或平卧坐起时，动作尽量缓慢，以免引起昏厥，有异常及时报告医生，调节用药。'),
            ('心动过缓','通过参加各种强度适宜的运动，使心功能得到锻炼，从而使静息心率逐渐恢复正常。一般适宜的运动心率是“170-年龄”，如一个50岁人，运动心率控制在120次/分钟为宜，过快说明运动量过大，达不到也起不到效果。运动前要自觉舒适、无疲劳感，一般运动不要超过1小时，而且每次最佳时间为30分钟～60分钟，每周至少坚持3次运动。'),
            ('心动过缓','改正不良的生活方式，熬夜、吸烟、饮酒，少喝浓茶，特别是不要在睡前喝，否则容易导致失眠。保持适当体重，体重过瘦、营养不良无法为心脏提供所需能量，因此体重过瘦、营养不良者要通过健身运动，调节饮食来保持适宜的体重。'),
            ('心动过缓','在心动过缓急性发作时，除针对原发病因进行治疗、停用可减慢心率的药物外，可以使用阿托品、异丙肾上腺素提高心率。对于心率在每分钟40次或者更慢者，药物提高心率效果不明显，尤其是伴有反复晕厥或晕厥前兆的患者，应置入心脏起搏器。'),
            ('心动过速','心率增快危害健康、缩短寿命，增加心血管病的发病率和死亡率。常参加各种强度适宜的运动，就会使静息心率变慢。虽然运动时心率加快，但运动能使心功能得到锻炼，从而使静息心率减慢。一般适宜的运动心率是“170-年龄”，如一个50岁人，运动心率控制在120次/分钟为宜，过快说明运动量过大，达不到也起不到效果。运动前要自觉舒适、无疲劳感，一般运动不要超过1小时，而且每次最佳时间为30分钟～60分钟，每周至少坚持3次运动。'),
            ('心动过速','改正不良的生活方式，熬夜、吸烟、饮酒均可使静息心率加快。少喝浓茶，特别是不要在睡前喝，否则容易导致失眠。还应定时大便，保持排便顺畅。保持适当体重，肥胖会使心脏负担加重，心率加快，因此肥胖者要通过健身运动，调节饮食来保持适宜的体重。保持心态要平和，避免着急、生气，出现心率过快时，可通过听音乐、静心冥想等方式逐渐恢复平静。'),
            ('心动过速','某些疾病如高血压及冠心病引起的心率加快，可根据医嘱服用药物，心律平、异搏定等可终止某些心动过速的发作，但不能根治，推注药物有一定危险性，不主张长期服药防止心动过速的再发。射频消融术可根治心动过速，术后不再需要使用抗心律失常药物；患者无痛苦，操作方法简便。特点是创伤小、恢复快，治愈率高。'),
            ('低脂血','在排除原发型疾病的基础上，建议改善饮食习惯，合理膳食，荤素搭配，适当多吃些禽蛋、海鲜、动物肝脏等高胆固醇类食物，适量增加锻炼，定期复查血脂变化，如果无变化建议全面身体检查。'),
            ('高脂血','高血脂患者在排除原发型疾病的基础上，需注意日常饮食、运动锻炼，以减少心脑血管疾病及其他相关疾病的发生风险。建议控制饮食，减少饱和脂肪酸（植物油、鱼油）和胆固醇摄入，每日摄入量<300mg；减少每日摄入脂肪量(<30g食用油)，增加膳食纤维，补充植物固醇和可溶性纤维，限制盐摄入量，戒烟，限制饮酒，禁饮烈性酒。'),
            ('高脂血','加强体育锻炼，进行每周5~7天每次30分钟中等强度体育运动。有心脑血管疾病、心血管疾病危险因素者、高血压、糖尿病、吸烟、过量饮酒、肥胖者、早发性心血管疾病家族史者、有家族性高脂血症者和皮肤或肌腱有黄色瘤人群建议定期监测血脂水平,非药物治疗一般情况下，每3~6个月复查1次血脂；如血脂达标，可延长至每6~12个月复查1次。调脂药物治疗6周内复查血脂、肝功能、肌酸激酶水平；如血脂达标，可延长至6~12个月复查1次；如血脂未达标，3个月后再次复查，仍未达标，调整治疗方案。'),
        )
    for intervent in intervents:
        hmtype=Indicator.objects.filter(name=intervent[0]).first()
        HealthIntervent.objects.get_or_create(hmtype = hmtype,intervent =intervent[1])

#创建用户组
def creatgroup():
    print('删除所有组......')
    Group.objects.all().delete()
    print('建立用户组：健康管理、个人用户 ......')
    #Group.objects.get(name='个人用户')
    if settings.LANGUAGE_CODE == 'en':
        usergroup=Group.objects.create(name='Personal User')
        healthgroup=Group.objects.create(name='Health Management')
    else:
        usergroup=Group.objects.create(name='个人用户')
        healthgroup=Group.objects.create(name='健康管理')

    print('用户组分配权限 ......')

    usertable=['userinfo', 'bodyinfo', 'bloodpressure','bcholesterin','smokediabetesinfo','contenttype']
    scaletable=['agescale', 'weightscale', 'bloodpressurescale', 'smokescale', 'diabetesscale', 'riskevaluatscale',
                'commonriskscale','tcscale','bmiscale','healthintervent','riskanalyse','singleassess','indicator','user']
    premissions = ['add', 'delete', 'change', 'view']
    for tb in usertable:
        for pm in premissions:
            pmtb = pm + '_' + tb
            perm = Permission.objects.get(codename=pmtb)
            usergroup.permissions.add(perm)
            healthgroup.permissions.add(perm)
    for tb in scaletable:
        for pm in premissions:
            pmtb = pm + '_' + tb
            perm = Permission.objects.get(codename=pmtb)
            healthgroup.permissions.add(perm)

#当django-adminlte-ui<v2.0.0版本时需在数据库中进行后台设置,>2.0.0版本时已不使用此方法
def creatsystemset():

    lines = [['site_title', '健康管理分析系统', True],
            ['site_header', '健康管理分析', True],
            ['welcome_sign', '欢迎使用健康管理分析系统！', True],
            ['avatar_field', 'request.user.head_avatar', False],
            ['show_avatar', 'on', True],
            ['USE_CUSTOM_MENU', '1', True],
            ['site_logo', 'medias/health-logo.png', True],
            ]
    for line in lines:
        newdata = Options.objects.get_or_create(option_name=line[0])
        if newdata:
            print(type(newdata))
            newdata[0].valid = line[2]
            newdata[0].option_value = line[1]          
            newdata[0].save()


    lines = [['000I',1,5,'健康信息','left',3,'/healthinfo/dashboard/',None,300,1,None],
            ['000I000S',2,0,'基本信息','left',0,'/admin/healthinfo/userinfo/',None,350,1,7],
            ['000I000W',2,0,'吸烟糖尿病史','left',0,'/admin/healthinfo/smokediabetesinfo/',None,340,1,7],
            ['000I000V',2,0,'身高体重信息','left',0,'/admin/healthinfo/bodyinfo/',None,330,1,7],
            ['000I000U',2,0,'血压信息','left',0,'/admin/healthinfo/bloodpressure/',None,320,1,7],
            ['000I000T',2,0,'血脂信息','left',0,'/admin/healthinfo/bcholesterin/',None,310,1,7],
            
            ['0006',1,13,'健康标准','left',3,None,None,400,1,None],
            ['00060027',2,0,'ICVD吸烟评估标准','left',0,'/admin/healthinfo/smokescale/',None,180,1,6],
            ['00060021',2,0,'ICVD年龄评估标准','left',0,'/admin/healthinfo/agescale/',None,200,1,6],
            ['00060026',2,0,'ICVD糖尿病评估标准','left',0,'/admin/healthinfo/diabetesscale/',None,170,1,6],
            ['00060020',2,0,'ICVD血压评估标准','left',0,'/admin/healthinfo/bloodpressurescale/',None,160,1,6],
            ['00060025',2,0,'ICVD体重评估标准','left',0,'/admin/healthinfo/weightscale/',None,190,1,6],
            ['0006001N',2,0,'ICVD十年发病风险常规标准','left',0,'/admin/healthinfo/commonriskscale/',None,130,1,6],
            ['0006001O',2,0,'ICVD十年发病风险评估标准','left',0,'/admin/healthinfo/riskevaluatscale/',None,140,1,6],
            ['00060023',2,0,'BMI体重健康评估标准','left',0,'/admin/healthinfo/bmiscale/',None,220,1,6],
            ['0006001W',2,0,'健康指标分类','left',0,'/admin/healthinfo/indicator/',None,120,1,6],
            ['0006001X',2,0,'健康风险分析','left',0,'/admin/healthinfo/riskanalyse/',None,110,1,6],
            ['00060024',2,0,'健康风险干预','left',0,'/admin/healthinfo/healthintervent/',None,100,1,6],
            ['0006002D',2,0,'单项评估标准','left',0,'/admin/healthinfo/singleassess/',None,210,1,6],
            ['00060022',2,0,'ICVD血脂评估标准','left',0,'/admin/healthinfo/tcscale/',None,150,1,6],

            ['0007',1,2,'认证授权','left',3,None,None,120,1,None],
            ['0007000A',2,0,'用户管理','left',0,'/admin/auth/user/',None,110,1,4],
            ['00070008',2,0,'组管理','left',0,'/admin/auth/group/',None,100,1,4],
            
            ['0008',1,3,'系统设置','left',3,None,None,110,1,None],
            ['0008000B',2,0,'基本设置','left',0,'/admin/django_admin_settings/options/general_option/',None,120,1,4],
            ['00080009',2,0,'菜单设置','left',0,'/admin/django_admin_settings/menu/',None,100,1,4],
            ['0008000A',2,0,'选项设置','left',0,'/admin/django_admin_settings/options/',None,110,1,4],
            
            ['000J',1,5,'健康评估','left',3,'/healthinfo/dashboard/',None,400,1,7],
            ['000J0011',2,0,'BMI体重健康评估','left',0,'/healthinfo/weightassess/',None,440,1,7],
            ['000J000Y',2,0,'血压健康评估','left',0,'/healthinfo/bpassess/',None,430,1,7],
            ['000J0010',2,0,'血脂健康评估','left',0,'/healthinfo/bsassess/',None,420,1,7],
            ['000J000N',2,0,'缺血性心血管病发病风险评估','left',0,'/healthinfo/icvdrisk/',None,410,1,7],
            ['000J000W',2,0,'日常习惯评估','left',0,'/healthinfo/habitassess/',None,450,1,7],
            
            ['0005',1,7,'健康分析','left',3,None,None,500,1,None],
            ['00050002',2,0,'分地区不良习惯及慢性病分析','left',0,'/healthinfo/analye/',None,500,1,6],
            ['00050004',2,0,'吸烟人群分布分析','left',0,'/healthinfo/smokeanalye/',None,560,1,6],
            ['00050005',2,0,'饮酒人群分布分析','left',0,'/healthinfo/drinkanalye/',None,550,1,6],
            ['0005000E',2,0,'糖尿病人群分布分析','left',0,'/healthinfo/diabetesanalye/',None,530,1,6],
            ['0005000H',2,0,'肥胖人群分布分析','left',0,'/healthinfo/fatanalye/',None,540,1,6],
            ['0005000G',2,0,'高血压人群分布分析','left',0,'/healthinfo/hypertensionanalye/',None,520,1,6],
            ['0005000I',2,0,'高脂血人群分布分析','left',0,'/healthinfo/hyperlipemanalye/',None,510,1,6],]
    for line in lines:
        if line[10] == 7:
            id=ContentType.objects.filter(app_label='contenttypes', model='contenttype').first()
        elif line[10] == 6:
            id = ContentType.objects.filter(app_label='auth', model='user').first()
        elif line[10] == 1:
            id = ContentType.objects.filter(app_label='auth', model='permission').first()
        else:
            id = None    
        newdata = Menu(path=line[0], depth=line[1], numchild=line[2],\
            name=line[3], position=line[4], link_type=line[5], link=line[6], icon=line[7], \
            priority_level=line[8], valid=line[9], content_type=id)
        newdata.save()


#创建超级用户
def create_superuser():
    
    print('建立超级用户：admin：health123')
    username='admin'
    password='health123'
    if not User.objects.filter(username=username).first():
        user=User.objects.create_superuser(username=username,password=password)
        if settings.LANGUAGE_CODE == 'en':
            group = Group.objects.get(name='Personal User') 
            group.user_set.add(user)
            group = Group.objects.get(name='Health Management') 
            group.user_set.add(user)
        else:
            group = Group.objects.get(name='个人用户') 
            group.user_set.add(user)
            group = Group.objects.get(name='健康管理') 
            group.user_set.add(user)
    else:
        print('admin已存在！')

#创建菜单
def creatmenu():
    pass


def main():

    print('创建用户组')
    creatgroup()
    print('删除所有用户......')
    User.objects.all().delete()
    print('创建超级用户')
    create_superuser()
    #
    #print('初始化系统设置')
    #creatsystemset()

    print('生成健康评价标准数据')
    createscale()

    num=30
    days=30
    t = TencentTranslate()
    print('随机生成{}个用户和{}天健康数据'.format(num,days))
    createuserdata(num=num,days=days,t=t)

if __name__ == "__main__":  
    print('System Init ...')
    main()
    print('Done!')