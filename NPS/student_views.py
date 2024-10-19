from django.shortcuts import render,redirect
from app.models import * 
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from app.decorators import student_required
from django.contrib import messages


@student_required

def STUDENT_HOME(request):
    student = request.user.student  # Assuming `request.user` is the logged-in student's user object

    # Calculate total days and present days
    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    notice = Notice.objects.all().order_by('-created_at')[:10]
    # Calculate attendance percentage
    attendance_percentage = f"{(present_days / total_days) * 100:.2f}" if total_days > 0 else "0"

    if request.user.is_authenticated and hasattr(request.user, 'student'):
        student_class = request.user.student.classes
        subjects = Subject.objects.filter(class_name=student_class)
    
    # Fetch all homeworks for the student's subjects
        homeworks = HomeWorks.objects.filter(subject__in=subjects).order_by('-uploaded_at')
    else:
        homeworks = []
               
    context = {
        'student': student,
        'total_days': total_days,
        'present_days': present_days,
        'attendance_percentage': attendance_percentage,
        'notice': notice,
        'homeworks': homeworks,
    }
    
    return render(request,'Student/student_home.html',context)


@student_required
def FEES(request):
    # student = get_object_or_404(Student, id=student_id)
    # fee_structure = FeeStructure.objects.get(class_name=student.classes)
    # fees, created = Fee.objects.get_or_create(student=student, defaults={'fee_structure': fee_structure})

    # context = {
    #     'student': student,
    #     'fees': fees,
    # }
    return render(request,'Student/fees.html')


@student_required
def STUDENT_VIEW(request):
    
    
    return render(request,'Student/student_view.html')

def PASSWORD_UPDATE(request):
    if request.method == "POST":
        
        email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')

    try:
        customuser = CustomUser.objects.get(id=request.user.id)

        # customuser.first_name = first_name
        # customuser.last_name = last_name
        
        if password !=None and password!= "":
                customuser.set_password(password)
        if email !=None and email!= "":
            customuser.email = email
        
        customuser.save()
        messages.success(request,'Your Profile Updated Successfully !')
        return redirect('login')
    except:
        messages.error(request,'Your Profile Updated Successfully  !')

    
    return render(request,'Student/student_view.html')



@student_required
def STUDENT_FORUM(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        student_class = request.user.student.classes
        subjects = Subject.objects.filter(class_name=student_class)
        notes_by_subject = {}
        

        for subject in subjects:
            notes = Notes.objects.filter(subject=subject)
            home_works = HomeWorks.objects.filter(subject=subject)
            if notes.exists():
                notes_by_subject[subject.subject_name] = notes[:2]
                
    else:
        notes_by_subject = {}  # No notes if the user is not authenticated or not a student

    context = {
            'notes_by_subject': notes_by_subject,
    }
           


    return render(request, 'Student/student_forum.html', context)


@student_required
def STUDENT_HOMWWORK(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        student_class = request.user.student.classes
        subjects = Subject.objects.filter(class_name=student_class)
        home_works_by_subject = {}

        for subject in subjects:
            home_works = HomeWorks.objects.filter(subject=subject)
            if home_works.exists():
                home_works_by_subject[subject.subject_name] = home_works[:2]
    else:
        home_works_by_subject = {}

    context = {'home_works_by_subject': home_works_by_subject
               }
    return render(request, 'Student/student_homework.html', context)


    

@student_required
def STUDENT_FORUM_EXTENDS(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    notes = Notes.objects.filter(subject=subject)


    context = {
        'subject': subject,
        'notes': notes,
    }
    return render(request, 'Student/student_forum_extends.html', context)

@student_required
def STUDENT_WORK_EXTENDS(request,subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    home_works = HomeWorks.objects.filter(subject=subject)
    context = {
        'subject': subject,
        'home_works': home_works,
        }
    return render(request, 'Student/student_homework_extends.html', context)

@student_required
def download_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    
    file_path = note.notes.path
    file_name = note.notes.name

    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    except FileNotFoundError:
        raise Http404("Note not found")

@student_required 
def download_homework(request, homework_id):
    homework = get_object_or_404(HomeWorks, id=homework_id)
    
    file_path = homework.homework.path
    file_name = homework.homework.name

    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    except FileNotFoundError:
        raise Http404("Note not found")
    
# def student_attendance_view(request):
#     student = request.user.student  # Assuming `request.user` is the logged-in student's user object

#     # Calculate total days and present days
#     total_days = Attendance.objects.filter(student=student).count()
#     present_days = Attendance.objects.filter(student=student, status='present').count()

#     # Calculate attendance percentage
#     attendance_percentage = (present_days / total_days) * 100 if total_days > 0 else 0

#     context = {
#         'student': student,
#         'total_days': total_days,
#         'present_days': present_days,
#         'attendance_percentage': attendance_percentage,
#     }

#     return render(request, 'student_portal/attendance.html', context)


from django.shortcuts import render
from .forms import studetPayment

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import razorpay

def student_payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        stu_class = request.POST.get('class')
        amount= float(request.POST.get('amount')) * 100
        #create Razorpay client 
        client = razorpay.Client(auth=('rzp_test_wFREsmnp7V1lQX','43kdOjXtmUDU1sExdYovP8aF'))
        
        #create an order 
        payment = client.order.create(dict(amount = amount,
                                                     currency = 'INR',)
                                                    )
        dbs = StudentsPayment(name = name , amount = amount , razorpay_payment_id = payment['id'])
        dbs.save()

    
        
        print(payment)
        print(name,stu_class,amount)
        return render(request,'student_payment.html' , {'payment':payment})
    return render(request,'student_payment.html')

@csrf_exempt
def payment_status(request):
    if request.method == "POST":
        a = request.POST
        order_id= ""
        for key, val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    student = StudentsPayment.objects.filter(payment_id =order_id).first()
    student.paid = True
    student.save()
    return render(request, 'payment_status.html')


@student_required
def FEEDBACK(request):
    if request.method == "POST":
        name = request.POST.get('name')
        classes = request.POST.get('classes')
        section = request.POST.get('section')
        subject = request.POST.get('subject')
        teacher_name = request.POST.get('teacher_name')
        rating = request.POST.get('rating')
        feedback_text = request.POST.get('feedback')
        
        feedback_save = Feedback(
            name=name,
            classes=classes,
            section=section,
            subject=subject,
            teacher_name=teacher_name,
            rating=rating,
            feedback=feedback_text
        )
        
        feedback_save.save()
        messages.success(request, "Your feedback has been submitted successfully!")
        return redirect('feedback')
    
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        student_class = request.user.student.classes
        subjects = Subject.objects.filter(class_name=student_class)
    
  
    context = {
            'subjects': subjects,
    }
    return render(request,'Student/feedback.html',context)


@student_required
def RESULT_VIEW(request):
    if request.user.user_type != '3':  # '3' represents Student in your USER choices
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})

    try:
        student = Student.objects.get(admin=request.user)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student profile not found.'})

    results = StudentResult.objects.filter(student=student)
    
    subjects = Subject.objects.filter(class_name=student.classes)
    
    result_dict = {}
    for subject in subjects:
        result = results.filter(subject=subject).first()
        if result:
            result_dict[subject] = result
        else:
            result_dict[subject] = None

    first_term_total = results.aggregate(Sum('first_term_marks'))['first_term_marks__sum'] or 0
    second_term_total = results.aggregate(Sum('second_term_marks'))['second_term_marks__sum'] or 0
    final_term_total = first_term_total + second_term_total
    
    context = {
        'student': student,
        'result_dict': result_dict,
        'first_term_total': first_term_total,
        'second_term_total': second_term_total,
        'final_term_total': final_term_total,
    }
    
    return render(request,'Student/result_view.html',context)
