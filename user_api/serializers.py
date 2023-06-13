from xml.dom import ValidationErr
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from . import models
#from ActivityPoints.user_api.models import Certificate, Student

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username','role')


class RegisterFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email','role']


class ViewAllFacultySerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username','role')

class FacultyLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	

class FacultyUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username','role')

class ViewAllStudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel 
		fields = '__all__'


class RegisterStudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ['username', 'email','role']
	
	
class StudentLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
   
class ViewAllCertificatesSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Certificate
		fields = '__all__'
	
class ViewPendingRequestsSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.PendingRequest
		fields = '__all__'

class ViewClassDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ClassDetail
		fields = '__all__'

class ViewAcitvityPointsSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ActivityPoint
		fields = '__all__'

