from xml.dom import ValidationErr
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ['email','username','role']
	def create(self, clean_data):
		clean_data['role'] = 'admin'

		user_obj = UserModel.objects.create_superuser(email=clean_data['email'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationErr('user not found')
		serializer = UserSerializer(user) 
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username','role')


class RegisterFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email','role']
	
    def create(self, clean_data):
        
        user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.role = 'faculty'
        user_obj.save()
        return user_obj
		
class ViewAllFacultySerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username','role')

