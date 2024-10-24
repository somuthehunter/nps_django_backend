"""
URL configuration for NPS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views,admin_views,staff_views,student_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.BASE,name='base'),


    #login
    path('login',views.LOGIN, name='login'),
    path('dologin', views.doLogin, name='doLogin'),
    path('dologout',views.doLogout, name='doLogout'),
    path('',views.HOME,name='home'),
    path('about',views.ABOUT,name='about'),
    path('gallary',views.GALLARY,name='gallary'),
    path('Enroll/',views.ENROLL,name='enroll'),
    path('Accountant/home',views.ACCOUNTANT_HOME,name='accountant'),

    #profile
    path('profile',views.PROFILE,name='profile'),
    path('profile/update',views.PROFILE_UPDATE, name='profile_update'),

    # admin 
    path('Admin/Home',admin_views.HOME, name='admin_home'),
    path('Admin/Student',admin_views.REGISTER_STUDENT, name='student_registration'),
    path('Admin/Student_registration/List/other-section-login/',admin_views.REGISTER_STUDENT_LIST,name="Student_registration_list"),
    path('Admin/Student_registration/bill-genrate/<str:id>',admin_views.REGISTER_STUDENT_BILL,name="Student_registration_bill"),
    path('Admin/Add-Teacher',admin_views.ADD_STAFF, name='add_teacher'),
    path('Admin/Teacher/list',admin_views.LIST_STAFF, name='list_teacher'),
    path('Admin/Teacher/edit/<str:id>',admin_views.EDIT_TEACHER,name='edit_teacher'),
    path('Admin/Teacher/update',admin_views.UPDATE_TEACHER,name='update_teacher'),
    path('Admin/Add-Student',admin_views.ADD_STUDENT, name='add_student'),
    path('Admin/Student/list',admin_views.LIST_STUDENT,name='list_student'),
    path('Admin/Student/view/<str:id>',admin_views.VIEW_STUDENT, name = "view_student"),
    path('Admin/Student/edit/<str:id>',admin_views.EDIT_STUDENT, name='edit_student'),
    path('Admin/Student/update',admin_views.UPDATE_STUDENT, name = "update_student"),
    #add
    path('delete_student/<int:student_id>/', admin_views.DELETE_STUDENT, name='delete_student'),
    path('Admin/fees_collection',admin_views.FEES_COLLECTION,name="fees_collection"),
    path('Admin/Fee/generate-bill/<int:student_id>/<str:month>/',admin_views.MONTHLY_FEES_BILL,name="monthly_fees_bill"),
    path('Admin/transport/fee/generate-bill/<int:student_id>/<str:month>/',admin_views.MONTHLY_TRANSPORT_BILL,name="monthly_transport_bill"),
    path('Admin/fees/update/<str:student_id>',admin_views.UPDATE_FEES,name="update_fees"),
    path('Admin/fee_structure/add',admin_views.ADD_FEE_STRUCTURE,name="add_fees_structure"),
    path('Admin/fee_structure/view',admin_views.VIEW_FEE_STRUCTURE,name="view_fees_structure"),
    path('Admin/Student/send_notification',admin_views.STUDENT_SEND_NOTIFICATION,name='student_send_notification'),
    path('Admin/view_attendance',admin_views.ADMIN_ATTENDANCE_VIEW,name="admin_view_attendance"),
    #adddd
    path('edit-attendance/<str:date>/<str:class_name>/<str:section>/', admin_views.EDIT_ATTENDANCE, name='edit_attendance'),
    # path('edit-attendance/', admin_views.EDIT_ATTENDANCE, name='edit_attendance'),
    path('Admin/transport',admin_views.TRANSPORT,name="transport"),
    path('Admin/transport/add',admin_views.ADD_TRANSPORT_FEE,name="add_transport_fee"),
    path('Admin/transport/delete/<int:id>/',admin_views.DELETE_TRANSPORT_FEE,name="delete_transport_fee"),
    path('Admin/transport/add/fees/<str:id>',admin_views.EDIT_STUDENT_TRANSPORT,name="edit_transport_fee"),
    path('Admin/fee/hostel',admin_views.HOSTEL,name="hostel"),
    path('Admin/hostel/add/fees/<str:id>',admin_views.EDIT_STUDENT_HOSTEL,name="edit_hostel_fee"),
    path('Admin/subject/view',admin_views.SUBJECT_VIEW,name="view_subject"),
    # path('Admin/update_transport_fees/<int:student_id>/', admin_views.UPDATE_TRANSPORT_FEES, name='update_transport_fees'),
    path('Admin/transport_fees/view',admin_views.VIEW_TRANSPORT_FEES,name="view_transport_fee"),
    path('Admin/Library',admin_views.LIBRARY,name="library"),
    path('Admin/Library/checkout',admin_views.CHECKOUT,name="checkout"),
    path('Admin/Library/generate_bill/<int:user_id>/',admin_views.generate_bill,name="generate_bill"),
    path('Admin/add_to_cart/<int:product_id>',admin_views.add_to_cart,name="add_to_cart"),
    path('Admin/cart/remove/<int:cart_item_id>/', admin_views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', admin_views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', admin_views.decrease_quantity, name='decrease_quantity'),
    path('generate_bill/', admin_views.generate_bill, name='generate_bill'),
    # path('view-bill/<int:bill_id>/', admin_views.view_bill, name='view_bill'),
    path('Admin/view/result',admin_views.ADMIN_RESULT_VIEW,name='admin_view_result'),
    path('Admin/Edit/Result/<int:result_id>/', admin_views.EDIT_RESULT, name='edit_result'),
    path('Admin/accounts_home',admin_views.ACCOUNTS_HOME,name='accounts_home'),
    path('Admin/hostel/fee/add',admin_views.ADD_HOSTEL_FEE,name="add_hostel_fee"),
    path('Admin/result',admin_views.RESULT,name="result"),
    path('Admin/result/marksheet',admin_views.GENERATE_MARKSHEET,name="marksheet"),
    path('Admin/result/print/marksheet/1st_term/<str:student_id>/',admin_views.PRINT_MARKSHEET_1,name="print_marksheet_1"),
    path('Admin/result/print/marksheet/<str:student_id>/',admin_views.PRINT_MARKSHEET,name="print_marksheet"),
    path('Admin/add/notifications',admin_views.add_notifications,name="add_notifications"),
    path('Admin/show/feedback',admin_views.ShowFeedback,name="show_feedback"),
    path('Admin/Enrolled/Student',admin_views.ENROLLED_STUDENT,name="enrolled_student"),
    path('Admin/Student/See',admin_views.STUDENT_SEE,name="student_see"),
    path('Admin/Library/Add-Items',admin_views.ADD_ITEMS,name="add_items"),
    path('Admin/Students/Enquiry',admin_views.ENQUIRY_STUDENT,name="enquiry_students"),
    path('Admin/Notice/Send',admin_views.SEND_NOTICE,name="send_notice"),
    path('account-section/login/', admin_views.account_section_login, name='account_section_login'),
    path('update_delete/', admin_views.update_delete, name='update_delete'),
    path('edit-product/<int:product_id>/', admin_views.edit_product, name='edit_product'),
    #adadddddd
    path('other-section/login/', admin_views.other_section_login, name='other_section_login'),
    path('Admin/accounts-add/',admin_views.ADD_ACCOUNTS,name="add_accounts"),
    path('Admin/generate-admit/',admin_views.GENERATE_ADMIT,name='generate_admit'),
    path('Admit/print-admit/<str:student_ids>/',admin_views.PRINT_ADMIT,name='print_admit'),
    path('Admin/add-routine/',admin_views.ADD_ROUTINE,name='add_routine'),
    path('Admin/delete-routine/<int:id>/',admin_views.DELETE_ROUTINE, name= 'delete_routine'),
    path('Admin/edit-routine/<int:id>/',admin_views.EDIT_ROUTINE, name= 'edit_routine'),
    path('Admin/delete-teacher/<int:id>/',admin_views.DELETE_TEACHER, name= 'delete_teacher'),
    # path('print-all-admit/', admin_views.PRINT_ALL_ADMIT, name='print_all_admit'),
    path('Admin/due-bill/',admin_views.DUE_BILL,name='due_bill'),
    path('Admin/due-bill/generate/',admin_views.GENERATE_DUE_BILL,name='generate_due_bill'),
    path('Admin/print-due-bill/',admin_views.PRINT_ALL_DUE_BILLS,name='print_all_due_bill'),
    path('filter-due-bills/', admin_views.FILTER_DUE_BILLS, name='filter_due_bills'),
    path('Admin/delete-feedback',admin_views.DELETE_FEEDBACK,name='delete_feedback'),
    path('student-section/login/', admin_views.student_section_login, name='student_section_login'),
    path('Admin/edit-transport-fee/<int:id>/',admin_views.EDIT_TRANSPORT_FEE,name="edit_transport_fees"),



    #staff
    path('Staff/Home',staff_views.STAFF_HOME, name='staff_home'),
    path('Staff/upload_notes',staff_views.UPLOAD_NOTES,name='upload_notes'),
    path('Staff/upload_home_works',staff_views.HOME_WORKS,name='home_works'),
    path('Staff/Take_Attendance',staff_views.STAFF_TAKE_ATTENDANCE,name="take_attendance"),
    path('Admin/Add/Result',staff_views.ADD_RESULT,name='add_result'),
    path('Admin/Edit/Result', staff_views.EDIT_RESULT, name='edit_result'),
    path('get_subjects/', staff_views.get_subjects, name='get_subjects'),



    #student
    path('Student/Home',student_views.STUDENT_HOME, name='student_home'),
    path('Student/fees',student_views.FEES,name="student_fees"),
    path('Student/student_forum',student_views.STUDENT_FORUM ,name="student_forum"),
    path('Student/Student/Home_work',student_views.STUDENT_HOMWWORK,name="home_work"),
    path('Student/student_notes/<int:subject_id>/',student_views.STUDENT_FORUM_EXTENDS,name="student_forum_extends"),
    path('Student/student_works/<int:subject_id>/',student_views.STUDENT_WORK_EXTENDS,name="student_work_extends"),
    path('download_note/<int:note_id>/', student_views.download_note, name='download_note'),
    path('download_homework/<int:homework_id>/', student_views.download_homework, name='download_homework'),
    path('Student/student_view',student_views.STUDENT_VIEW,name='student_view'),
    path('Student/payment',student_views.student_payment,name='student-payment' ),
    path('Student/feedback',student_views.FEEDBACK,name="feedback"),
    path('Student/result',student_views.RESULT_VIEW,name="result_view"),
    path('Student/password/update',student_views.PASSWORD_UPDATE,name="update_password"),


    


 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
