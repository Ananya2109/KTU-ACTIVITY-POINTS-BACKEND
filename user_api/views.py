from sys import api_version
from urllib import response
from django.contrib.auth import get_user_model, login, logout,  authenticate
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserModel,PendingRequestActionSerializer, UserRegisterSerializer,ViewAllStatusSerializer, GraduationYearSerializer,BranchesSerializer, RegisterStudentSerializer,UserLoginSerializer, StudentLoginSerializer, UserSerializer, RegisterFacultySerializer, ViewAllFacultySerializer, FacultyLoginSerializer, FacultyUserSerializer, ViewAllStudentSerializer, RegisterStudentSerializer, ViewAllCertificatesSerializer, ViewPendingRequestsSerializer, ViewClassDetailsSerializer, ViewAcitvityPointsSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import ActivityPoint, AppUser,Status,PendingRequest, Branch, Certificate, ClassDetail, GraduationYear, PendingRequest, Student
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




class UploadCertificate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = ViewAllCertificatesSerializer
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        serializer = ViewAllCertificatesSerializer(Certificate.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        #data = json.loads(request.body.decode('utf-8'))
        #uploaded_file = request.FILES.get('file')
        
        print(request.FILES)
        print(request.data)
        user = UserModel.objects.get(user_id = request.data.get('user'))
        activity_type = ActivityPoint.objects.get(id = request.data.get('activity_type'))
        certificate_approval_status = Status.objects.get(status= "pending")
        student_object = Student.objects.get(user=user)
        print(student_object.class_detail.branch)
        #class_detail_object = ClassDetail.objects.get(student_object.class_detail.id)
        # branch_object = Branch.objects.get(id=class_detail_object.branch)
        # print(class_detail_object)
        uploaded_file = request.FILES.get('file')

        
        cert_obj = Certificate.objects.create(
            user=user,
            activity_point_details = activity_type,
            uploaded_file = uploaded_file,
            certificate_approval_status = certificate_approval_status
        )
        cert_obj.save()
        
    #     class PendingRequest(models.Model):
    # certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    # student_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='pending_requests')
    # faculty = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    # grad_year = models.ForeignKey('GraduationYear', on_delete=models.CASCADE)
    # branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    # status = models.ForeignKey('Status', on_delete=models.CASCADE)
    
        pending_request_object = PendingRequest.objects.create(
            certificate = cert_obj,
            student_user = user,
            faculty  = student_object.class_detail.user,
            grad_year = student_object.class_detail.grad_year,
            branch =  student_object.class_detail.branch,
            status = certificate_approval_status
        )
        pending_request_object.save()
        
        #serializer = ViewAllCertificatesSerializer(data=data)
        if cert_obj:
                return Response("Certificate has been uploaded", status=status.HTTP_201_CREATED)
        
        return Response("Error in uploading certificate", status=status.HTTP_400_BAD_REQUEST)

class CertificateStatus(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Status.objects.all()
    serializer_class = ViewAllStatusSerializer
    

class PendingRequestAction(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = PendingRequestActionSerializer
   
    def post(self, request):
        pending_request_object = PendingRequest.objects.get(id = request.data['id'])
        certificate_approval_status = Status.objects.get(id= request.data['status_id'])
        student_object = Student.objects.get(user = pending_request_object.student_user) 
        if certificate_approval_status.status == "approved":
            pending_request_object.status = certificate_approval_status
            
            student_object.point_scored = student_object.point_scored + pending_request_object.certificate.activity_point_details.point_alloted
            student_object.save()
            pending_request_object.save()
        if certificate_approval_status.status == "rejected":
            pending_request_object.status = certificate_approval_status
            pending_request_object.save() 
        
        if pending_request_object:
               return Response(f"Updated points are : {student_object.point_scored} ", status=status.HTTP_201_CREATED)
        return Response("Request Failed", status=status.HTTP_400_BAD_REQUEST)



# user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
#     certificate_approval_status = models.ForeignKey('Status', on_delete=models.CASCADE)
#     activity_point_details = models.ForeignKey('ActivityPoint', on_delete=models.CASCADE)
#     uploaded_file = models.FileField(upload_to='certificates/',null=True, default=None)  # Added attribute for file upload

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
        faculty_class_details = ClassDetail.objects.get(user = data['user_id'])

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
            print(user_obj)
            user_obj.save()
            student_obj = Student.objects.create(user = user_obj,class_detail= faculty_class_details)
            student_obj.save()
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
    permission_classes = (permissions.AllowAny,)
    queryset = Student.objects.all()
    serializer_class = ViewAllStudentSerializer

    
# class ViewAllCertificates(generics.ListAPIView):
#     queryset = Certificate.objects.all()
#     serializer_class = ViewAllCertificatesSerializer
#     def post(self, request):
#         clean_data = custom_validation(request.data)
#         serializer = ViewAllCertificatesSerializer(data=clean_data)
#         if serializer.is_valid(raise_exception=True):
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewPendingRequests(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = PendingRequest.objects.all()
    serializer_class = ViewPendingRequestsSerializer
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = ViewPendingRequestsSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewClassDetails(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,request):
        data = ClassDetail.objects.all()
        print(data)
        resp = ViewClassDetailsSerializer(data,many=True)
        return Response(resp.data, status=status.HTTP_200_OK)

    def post(self, request):
        clean_data = request.data
        serializer = ViewClassDetailsSerializer(data=clean_data)

        if serializer.is_valid(raise_exception=True):
            branch = Branch.objects.get(id = clean_data['branch'])
            user = AppUser.objects.get(user_id = clean_data['user'])
            grad_year = GraduationYear.objects.get(id = clean_data['grad_year'])
            details = ClassDetail.objects.create(branch = branch, user = user, grad_year=grad_year)
            details.save()
            if details:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewActivityPoints(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = ActivityPoint.objects.all()
    serializer_class = ViewAcitvityPointsSerializer
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = ViewAcitvityPointsSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
###########################################
# USE THIS TO SAVE THE BRANCHES,YEAR VALUES   
# AFTER DELETEING DB
#  for choice_value, choice_label in Branch.BRANCH_CHOICES:
#     branch = Branch.objects.create(branch=choice_value)
# 
# for choice_value, choice_label in GraduationYear.grad_year_choice:
#     grad_year = GraduationYear.objects.create(grad_year=choice_value)

                    
###########################################

class Branches(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Branch.objects.all()
    serializer_class = BranchesSerializer


class GradYear(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = GraduationYear.objects.all()
    serializer_class = GraduationYearSerializer

