from django.shortcuts import render,redirect
from app.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from datetime import date
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def STAFF_HOME(request):
    return render(request,'Staff/staff_home.html')

@login_required(login_url='/')
def UPLOAD_NOTES(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher_name')
        notes_file = request.FILES.get('notes')
        note_name = request.POST.get('note_name')


            
            # Get the Subject and Teacher instances
        subject = Subject.objects.get(id=subject_id)
        # teacher = Teacher.objects.get(admin_id=teacher_id)  # Use admin_id for ForeignKey reference

            # Create and save the Notes instance
        notes = Notes(subject=subject, teacher_name=teacher_id, notes=notes_file,note_name=note_name)
        notes.save()

        # Optionally add a success message or redirect
        messages.success(request,'Notes uploaded Successfully !')
        return redirect('upload_notes')  # Replace 'some-view-name' with the name of the view you want to redirect to

        

    context = {
        'subjects': subjects,
        'teachers': teachers,
    }
    return render(request, 'Staff/upload_notes.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.conf import settings
import os
from docx import Document
from io import BytesIO
import html2text

@login_required(login_url='/')
def HOME_WORKS(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher_name')
        homework_name = request.POST.get('homework_name')
        content_type = request.POST.get('content_type')

        subject = Subject.objects.get(id=subject_id)

        if content_type == 'file':
            homework = request.FILES.get('homework')
            if homework:
                notes = HomeWorks(
                    subject=subject,
                    teacher_name=teacher_id,
                    homework_name=homework_name
                )
                notes.homework.save(homework.name, homework)
                notes.save()
                messages.success(request,"Homework updated Successfully ! ")

            else:
                return render(request, 'Staff/home_works.html', {'error': 'No file was uploaded.'})

        elif content_type == 'text':
            rich_text_content = request.POST.get('rich_text_content')
            
            # Convert HTML to plain text
            h = html2text.HTML2Text()
            h.ignore_links = False
            plain_text_content = h.handle(rich_text_content)
            
            # Convert plain text to .docx
            doc = Document()
            doc.add_paragraph(plain_text_content)
            
            # Save the document to a BytesIO object
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            # Create a unique filename
            file_name = f"{homework_name}.docx"

            # Create HomeWorks object and save the file
            notes = HomeWorks(
                subject=subject,
                teacher_name=teacher_id,
                homework_name=homework_name
            )
            notes.homework.save(file_name, ContentFile(buffer.getvalue()))
            notes.save()
            messages.success(request,"Homework updated Successfully ! ")


        return redirect('home_works')

    context = {
        'subjects': subjects,
        'teachers': teachers,
    }

    return render(request, 'Staff/home_works.html', context)


@login_required(login_url='/')
def DAILY_WORKS(request):

    return render(request,'Staff/daily_works.html')

@login_required(login_url='/')
def STAFF_TAKE_ATTENDANCE(request):
    class_choices = Student.class_choices
    section_choices = Student.section_choices
    action = request.GET.get('action')

    if action == 'get_student':
        if request.method == "POST":
            classes = request.POST.get('classes')
            section = request.POST.get('section')
            students = Student.objects.filter(classes=classes,section=section)
            context = {
                'action': 'take_attendance',
                'class_choices': class_choices,
                'section_choices': section_choices,
                'students': students,
            }
            return render(request, 'Staff/staff_take_attendance.html', context)

    elif action == 'submit_attendance':
        if request.method == "POST":
            date_input = request.POST.get('date')
            classes = request.POST.get('classes')
            students = Student.objects.filter(classes=classes)

            for student in students:
                status = 'present' if request.POST.get(f'student_{student.id}') else 'absent'
                attendance, created = Attendance.objects.get_or_create(
                    student=student,
                    date=date_input,
                    defaults={'status': status}
                )
                if not created:
                    attendance.status = status
                    attendance.save()
                print(f"Attendance for {student.admin.first_name} {student.admin.last_name}: {status} (created: {created})")
            messages.success(request,f"{date_input} Attendance Uploaded Successfully !")
            return redirect('take_attendance')  # Redirect to a success page

    context = {
        'action': action,
        'class_choices': class_choices,
        'section_choices': section_choices,
    }

    return render(request, 'Staff/staff_take_attendance.html', context)


@login_required(login_url='/')
def ADD_RESULT(request):
    action = request.GET.get('action', None)
    students = []
    subjects = []
    
    # Initialize filter form
    filter_form = ResultFilterForm(request.POST or None)
    
    if request.method == "POST":
        if action == "get_student" and filter_form.is_valid():
            class_name = filter_form.cleaned_data['class_name']
            section = filter_form.cleaned_data['section']
            subject = filter_form.cleaned_data['subject']
            exam_term = filter_form.cleaned_data['exam_term']

            # Filter students based on form data
            students = Student.objects.filter(classes=class_name, section=section)
            
            # Filter subjects based on class_name
            subjects = Subject.objects.filter(class_name=class_name)
            
            if subject:
                subjects = subjects.filter(id=subject.id)
            
            
            # Store filter data to re-use in the result entry form
            context = {
                'action': 'get_student',
                'students': students,
                'subjects': subjects,
                'filter_form': filter_form
            }
            return render(request, 'Staff/add_result.html', context)
        
        elif action == "add_result":
            exam_term = request.POST.get('exam_term')
            for key, value in request.POST.items():
                if key.startswith("student_"):
                    student_id = key.split("_")[1]
                    subject_id = key.split("_")[2]
                    
                    # Retrieve or create the StudentResult object
                    student_result, created = StudentResult.objects.get_or_create(
                        student_id=student_id,
                        subject_id=subject_id,
                    )

                    if exam_term == "first_term":
                        FA_I = request.POST.get(f"FA_I_{student_id}_{subject_id}")
                        NB_I = request.POST.get(f"NB_I_{student_id}_{subject_id}")
                        SE_I = request.POST.get(f"SE_I_{student_id}_{subject_id}")
                        first_term_marks = request.POST.get(f"first_term_marks_{student_id}_{subject_id}")
                        
                        if FA_I:
                            student_result.FA_I = int(FA_I)
                        if NB_I:
                            student_result.NB_I = int(NB_I)
                        if SE_I:
                            student_result.SE_I = int(SE_I)
                        if first_term_marks:
                            student_result.first_term_marks = int(first_term_marks)
                        
                        student_result.save()
                    
                    elif exam_term == "second_term":
                        FA_II = request.POST.get(f"FA_II_{student_id}_{subject_id}")
                        NB_II = request.POST.get(f"NB_II_{student_id}_{subject_id}")
                        SE_II = request.POST.get(f"SE_II_{student_id}_{subject_id}")
                        second_term_marks = request.POST.get(f"second_term_marks_{student_id}_{subject_id}")
                        
                        if FA_II:
                            student_result.FA_II = int(FA_II)
                        if NB_II:
                            student_result.NB_II = int(NB_II)
                        if SE_II:
                            student_result.SE_II = int(SE_II)
                        if second_term_marks:
                            student_result.second_term_marks = int(second_term_marks)
                        
                        student_result.save()

            messages.success(request,'Result Added Successfully !')
            return redirect('add_result')
        
    
    # Initial load or when no action is provided
    context = {
        'action': action,
        'students': students,
        'subjects': subjects,
        'filter_form': filter_form
    }
    return render(request, 'Staff/add_result.html', context)

from django.http import JsonResponse

def get_subjects(request):
    class_name = request.GET.get('class_name')
    subjects = Subject.objects.filter(class_name=class_name).values('id', 'subject_name')
    return JsonResponse(list(subjects), safe=False)

@login_required(login_url='/')
def EDIT_RESULT(request):
    action = request.GET.get('action', None)
    students = []
    subjects = Subject.objects.all()
    results = {}
    
    # Initialize filter form
    filter_form = FilterForm(request.POST or None)
    
    if request.method == "POST":
        if action == "get_student" and filter_form.is_valid():
            class_name = filter_form.cleaned_data['class_name']
            section = filter_form.cleaned_data['section']
            subject = filter_form.cleaned_data['subject']
            exam_term = filter_form.cleaned_data['exam_term']

            # Filter students based on form data
            students = Student.objects.filter(classes=class_name, section=section)
            
            if subject:
                subjects = Subject.objects.filter(id=subject.id)
            else:
                subjects = Subject.objects.all()
                
            # Fetch existing results for the selected students and subjects
            results = StudentResult.objects.filter(
                student__in=students,
                subject__in=subjects
            ).values('student_id', 'subject_id', 'first_term_marks', 'second_term_marks')
            
            # Reorganize results into a dictionary for easy lookup
            result_dict = {}
            for result in results:
                key = (result['student_id'], result['subject_id'])
                result_dict[key] = result
                
            context = {
                'action': 'edit_result',
                'students': students,
                'subjects': subjects,
                'filter_form': filter_form,
                'results': result_dict,
                'exam_term': exam_term
            }
            return render(request, 'Staff/edit_result.html', context)
        
        elif action == "update_result":
            for key, value in request.POST.items():
                if key.startswith("student_"):
                    student_id = key.split("_")[1]
                    subject_id = key.split("_")[2]
                    first_term_marks = request.POST.get(f"first_term_marks_{student_id}_{subject_id}")
                    second_term_marks = request.POST.get(f"second_term_marks_{student_id}_{subject_id}")

                    first_term_marks = int(first_term_marks) if first_term_marks else 0
                    second_term_marks = int(second_term_marks) if second_term_marks else 0
                    StudentResult.objects.update_or_create(
                        student_id=student_id,
                        subject_id=subject_id,
                        defaults={
                            'first_term_marks': first_term_marks,
                            'second_term_marks': second_term_marks,
                        }
                    )
            return redirect('edit_result')

    # Initial load or when no action is provided
    context = {
        'action': action,
        'students': students,
        'subjects': subjects,
        'filter_form': filter_form
    }
    return render(request, 'Staff/edit_result.html', context)

