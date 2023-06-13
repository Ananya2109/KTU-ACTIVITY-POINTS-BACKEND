from sys import api_version
from django.contrib.auth import get_user_model, login, logout,  authenticate
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserModel, UserRegisterSerializer, RegisterStudentSerializer,UserLoginSerializer, StudentLoginSerializer, UserSerializer, RegisterFacultySerializer, ViewAllFacultySerializer, FacultyLoginSerializer, FacultyUserSerializer, ViewAllStudentSerializer, RegisterStudentSerializer, ViewAllCertificatesSerializer, ViewPendingRequestsSerializer, ViewClassDetailsSerializer, ViewAcitvityPointsSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import ActivityPoint, AppUser, Certificate, ClassDetail, PendingRequest, Student
from rest_framework import generics
import json

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user_obj = UserModel.objects.create_superuser(email=clean_data['email'], password=clean_data['password'])
            user_obj.username = clean_data['username']
            user_obj.role = 'admin'
            user_obj.save()
            if user_obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    ##
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=data['email'], password=data['password'])
            if not user:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'user_id':user.user_id}, status=status.HTTP_200_OK)
    

class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    ##
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class RegisterFaculty(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        user = UserModel.objects.get(user_id = data['user_id'])
        if not user:
            return Response("Only admins can register faculty.",status=status.HTTP_400_BAD_REQUEST)

        if not user.role == 'admin':
            return Response("Only admins can register faculty.",status=status.HTTP_400_BAD_REQUEST)
        
        clean_data = custom_validation(data)
        serializer = RegisterFacultySerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
            user_obj.username = clean_data['username']
            user_obj.role = 'faculty'
            user_obj.save()
            if user_obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewAllFaculty(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    
    queryset = UserModel.objects.filter(role='faculty')
    serializer_class = ViewAllFacultySerializer


class FacultyLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = FacultyLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=data['email'], password=data['password'])
            if not user:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'user_id':user.user_id}, status=status.HTTP_200_OK)
    


class FacultyLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class FacultyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    ##
    def get(self, request):
        serializer = FacultyUserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class RegisterStudent(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print("data is: ", data)
        user = UserModel.objects.get(user_id = data['user_id'])
        if not user:
            return Response("Only the faculty can register students.",status=status.HTTP_400_BAD_REQUEST)

        if not user.role == 'faculty':
            return Response("Only faculty can register student.",status=status.HTTP_400_BAD_REQUEST)
        
        clean_data = custom_validation(request.data)
        serializer = RegisterStudentSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
            user_obj.username = clean_data['username']
            user_obj.role = 'student'
            user_obj.save()
            if user_obj:
               return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = StudentLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=data['email'], password=data['password'])
            if not user:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'user_id':user.user_id}, status=status.HTTP_200_OK)
          
class ViewAllStudent(generics.ListAPIView):
    
    queryset = UserModel.objects.filter(role='student')
    serializer_class = ViewAllStudentSerializer

    
class ViewAllCertificates(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = ViewAllCertificatesSerializer
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = ViewAllCertificatesSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewPendingRequests(generics.ListAPIView):
    queryset = PendingRequest.objects.all()
    serializer_class = ViewPendingRequestsSerializer
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = ViewPendingRequestsSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewClassDetails(generics.ListAPIView):
    queryset = ClassDetail.objects.all()
    serializer_class = ViewClassDetailsSerializer
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = ViewClassDetailsSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewActivityPoints(generics.ListAPIView):
    queryset = ActivityPoint.objects.all()
    serializer_class = ViewAcitvityPointsSerializer
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = ViewAcitvityPointsSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    