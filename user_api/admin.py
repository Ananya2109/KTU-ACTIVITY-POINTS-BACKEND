from django.contrib import admin
from user_api.models import AppUser, Student, ClassDetail, Certificate, ActivityPoint, PendingRequest, Branch, GraduationYear, Status
# Register your models here.
admin.site.register(AppUser)
admin.site.register(Student)
admin.site.register(ClassDetail)
admin.site.register(Certificate)
admin.site.register(ActivityPoint)
admin.site.register(PendingRequest)
admin.site.register(Branch)
admin.site.register(GraduationYear)
admin.site.register(Status)


