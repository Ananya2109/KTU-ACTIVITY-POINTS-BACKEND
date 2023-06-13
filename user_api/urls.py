from django.urls import path
from . import views

urlpatterns = [
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
	path('register-faculty', views.RegisterFaculty.as_view(), name='register-faculty'),
	path('view-faculty', views.ViewAllFaculty.as_view(), name='view-faculty'),
	path('faculty-login', views.FacultyLogin.as_view(), name='faculty-login'),
	path('faculty-logout', views.FacultyLogout.as_view(), name='faculty-logout'),
	path('faculty-view', views.FacultyView.as_view(), name='faculty-view'),
	path('student', views.ViewAllStudent.as_view(), name='student'),
	path('certificate', views.ViewAllCertificates.as_view(), name='certificate'),
	path('pending-request', views.ViewPendingRequests.as_view(), name='pending-request'),
	path('class-details', views.ViewClassDetails.as_view(), name='class-details'),
	path('activity-points', views.ViewActivityPoints.as_view(), name='activity-points'),
	path('register-student', views.RegisterStudent.as_view(), name='register-student'),
	path('view-students', views.ViewAllStudent.as_view(), name='view-student'),
	path('student-login', views.StudentLogin.as_view(), name='student-login'),
	path('branches', views.Branches.as_view(),name='branches'),
	path('gradyear', views.GradYear.as_view(),name='gradyear'),
	
]
	