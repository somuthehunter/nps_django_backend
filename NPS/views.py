from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from app.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout 
from app.models import *
from django.contrib.auth.decorators import login_required
from maintenance_mode.decorators import force_maintenance_mode_off, force_maintenance_mode_on

def BASE(request):
    # notifications = []
    # if request.user.is_authenticated and hasattr(request.user, 'student'):
    #     student_class = request.user.student.classes
    #     notifications = Student_Notification.objects.filter(class_name=student_class).order_by('-sent_at')
    # context = {'notifications': notifications}
    return render(request, 'base.html')
@force_maintenance_mode_off
def HOME(request):
    academic_notice = Notice.objects.filter(types="Academic").order_by('-created_at')
    hostel_notice = Notice.objects.filter(types="Hostel").order_by('-created_at')
    transport_notice = Notice.objects.filter(types="Transport").order_by('-created_at')

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        student_enquiry = Enquiry(name=name,phone=phone,message=message)
        student_enquiry.save()
        messages.success(request, "Your message has been sent successfully")
        return redirect('home')
    context={
        'academic_notice':academic_notice,
        'hostel_notice':hostel_notice,
        'transport_notice':transport_notice,
    }
    return render(request, 'Server/home.html',context)

def ABOUT(request):
    return render(request, 'Server/about.html')



def GALLARY(request):
    # Retrieve all media files from the database
    media_files = Media.objects.all()
    # print(media_files.media_type)
    

    return render(request, 'Server/gallary.html', {'media_files': media_files})






# def ENQUIRY(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         student_enquiry = Enquiry(name=name,email=email,phone=phone,message=message)
#         student_enquiry.save()
#         messages.success(request, "Your message has been sent successfully")
#         return redirect('student_enquiry')
#     return render(request, "Admin/student_enquiry.html")

def ENROLL(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        father_name = request.POST.get('father_name')
        student_class = request.POST.get('class')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        question = request.POST.get('question')
    
        enroll = Enrollment(
            student_name = student_name , 
            father_name = father_name,
            student_class = student_class,
            email = email,
            mobile = mobile, 
            question = question
        )
        enroll.save()
        return render(request,'Server/enroll.html')


    return render(request,'Server/enroll.html')

def LOGIN(request):
    return render(request,'login.html')


def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username= request.POST.get('email'),
                                         password=request.POST.get('password'),)
        if user!= None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            elif user_type == '4':
                return redirect('accountant')
            else:
                messages.error(request,'Email and Password are Invalid !')
                return redirect('login')
        else:   
            messages.error(request,'Email and Password are Invalid !')     
            return redirect('login')
        
def doLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)

    context ={
        "user" : user,
    }
    return render(request,'profile.html',context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')

    try:
        customuser = CustomUser.objects.get(id=request.user.id)

        customuser.first_name = first_name
        customuser.last_name = last_name
        
        if password !=None and password!= "":
                customuser.set_password(password)
        if profile_pic !=None and profile_pic!= "":
                customuser.profile_pic = profile_pic
        customuser.save()
        messages.success(request,'Your Profile Updated Successfully !')
        return redirect('profile')
    except:
        messages.error(request,'Your Profile Updated Successfully  !')

    return render(request,'profile.html')


def ACCOUNTANT_HOME(request):
    return render(request,'accountant_home.html')


