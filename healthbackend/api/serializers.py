from django.contrib.auth.models import User,Group,Permission
from rest_framework import serializers,validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from healthmanage.models import *

# 用户注册序列化
class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(label='确认密码', help_text='确认密码',
                                             min_length=6, max_length=20,
                                             write_only=True,
                                             error_messages={
                                                 'min_length': '仅允许6~20个字符的确认密码',
                                                 'max_length': '仅允许6~20个字符的确认密码', })
    token = serializers.CharField(label='生成token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_confirm', 'token')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的用户名',
                    'max_length': '仅允许6-20个字符的用户名',
                }
            },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'write_only': True,
                'required': True,
                # 添加邮箱重复校验
                'validators': [validators.UniqueValidator(queryset=User.objects.all(), message='此邮箱已注册')],
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的密码',
                    'max_length': '仅允许6-20个字符的密码',
                }
            }
        }

    # 多字段校验：直接使用validate，但是必须返回attrs
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('密码与确认密码不一致')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        # 创建user模型对象
        user = User.objects.create_user(**validated_data)

        # 创建token
        #payload = jwt_payload_handler(user)
        #token = jwt_encode_handler(payload)

        user.token = MyTokenObtainPairSerializer.get_token(user)
        return user


# 自定义token内容

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # 添加额外信息
        token['username'] = user.username
        return token
'''
# 用户注册序列化
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
'''

# restAPI序列化
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        #read_only_fields = ('id')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        #read_only_fields = ('id')

class UserSerializer(serializers.ModelSerializer):
    #author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = '__all__'
        #read_only_fields = ('id')
        
class UserInfoSerializer(serializers.ModelSerializer):
    #author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserInfo
        fields = '__all__'
        #read_only_fields = ('id')

class SmokeDiabetesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmokeDiabetesInfo
        fields = '__all__'
        #read_only_fields = ('id')

class BodyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyInfo
        fields = '__all__'

class BloodPressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodPressure
        fields = '__all__'
        
class BcholesterinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bcholesterin
        fields = '__all__'
        
class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'
        
class AgeScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeScale
        fields = '__all__'
        
class WeightScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightScale
        fields = '__all__'
        
class BloodPressureScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodPressureScale
        fields = '__all__'
        
class TCScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCScale
        fields = '__all__'
        
class SmokeScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmokeScale
        fields = '__all__'
        
class DiabetesScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiabetesScale
        fields = '__all__'
        
class RiskEvaluatScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskEvaluatScale
        fields = '__all__'
        
class CommonRiskScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonRiskScale
        fields = '__all__'
        
class BMIScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BMIScale
        fields = '__all__'
        
class SingleAssessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleAssess
        fields = '__all__'
        
class RiskAnalyseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAnalyse
        fields = '__all__'
        
class HealthInterventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIntervent
        fields = '__all__'
        

