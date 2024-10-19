from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# from django.contrib.auth.admin import UserAdmin
# from import_export.admin import ImportExportModelAdmin

# class UserModel(UserAdmin):
#     list_display = ['username','user_type']
# admin.site.register(CustomUser,UserModel)

# Register your models here.
@admin.register(CustomUser)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','username' ,  'email']

@admin.register(Student)
class StudentModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','admin','classes','section']
    list_filter = ['classes']
    search_fields = ['classes','section','admin']

@admin.register(Teacher)
class TeacherModelAdmin(admin.ModelAdmin):
    list_display= ['id','admin' ]


@admin.register(Fee)
class FeeModelAdmin(admin.ModelAdmin):
    list_display = [ 'id','student']
    list_filter = ['student']
    search_fields = ['student']
    

@admin.register(FeeStructure)
class FeeStructureModelAdmin(admin.ModelAdmin):
    list_display = ['id','class_name','amount']

@admin.register(StudentResult)
class StudentResultModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','student','subject']
    list_filter = ['subject']

# admin.site.register(StudentResult)


@admin.register(Subject)
class SubjectModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','subject_name']
    
admin.site.register(Notes)
admin.site.register(HomeWorks)
admin.site.register(Staff_Notification)
admin.site.register(Student_Notification)
admin.site.register(Attendance)
# admin.site.register(Attendance_Report)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Transport_Fees)
admin.site.register(HostelFee)
admin.site.register(StudentsPayment)
admin.site.register(StudentRegistration)
admin.site.register(Feedback)
admin.site.register(Enrollment)
admin.site.register(Enquiry)
admin.site.register(Notice)
admin.site.register(Routine)
admin.site.register(Session)
