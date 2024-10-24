from django.shortcuts import render,redirect,HttpResponse
from app.models import * 
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
from .forms import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import os
from django.contrib.auth.decorators import login_required
from num2words import num2words
from app.decorators import admin_required,account_section_required,other_section_required,student_section_required
from django.conf import settings

@admin_required
def HOME(request):
    student = Student.objects.all().count()
    teacher = Teacher.objects.all().count()
    register_student = StudentRegistration.objects.all().count()
    context = {
        'student':student,
        'teacher':teacher,
        'register_student':register_student,
    }
    return render(request, 'Admin/home.html',context)

@admin_required
@other_section_required
def REGISTER_STUDENT_BILL(request,id):
    try:
        student_registration = StudentRegistration.objects.filter(id=id)
    except StudentRegistration.DoesNotExist:
        student_registration = None
        messages.error(request, "Student Registration not found.")

    return render(request, 'Admin/student_registration_bill.html', {'student_registration': student_registration})


@admin_required
@other_section_required
def REGISTER_STUDENT(request):
    class_choices = Student.class_choices
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        class_for = request.POST.get('class_for')
        date_of_entry = request.POST.get('date_of_entry')
        last_school_attended = request.POST.get('last_school_attended')
        last_class_attended = request.POST.get('last_class_attended')
        last_examination_attended = request.POST.get('last_examination_attended')
        result = request.POST.get('result')
        mothers_name = request.POST.get('mothers_name')
        mothers_occupation = request.POST.get('mothers_occupation')
        mothers_occupation_other = request.POST.get('mothers_occupation_other')
        mothers_qualification = request.POST.get('mothers_qualification')
        mothers_qualification_other = request.POST.get('mothers_qualification_other')
        mothers_mobile_no = request.POST.get('mothers_mobile_no')
        fathers_name = request.POST.get('fathers_name')
        fathers_occupation = request.POST.get('fathers_occupation')
        fathers_occupation_other = request.POST.get('fathers_occupation_other')
        fathers_qualification = request.POST.get('fathers_qualification')
        fathers_qualification_other = request.POST.get('fathers_qualification_other')
        fathers_mobile_no = request.POST.get('fathers_mobile_no')
        local_guardian = request.POST.get('local_guardian')
        local_guardian_other = request.POST.get('local_guardian_other')
        local_guardian_occupation = request.POST.get('local_guardian_occupation')
        local_guardian_occupation_other = request.POST.get('local_guardian_occupation_other')
        local_guardian_qualification = request.POST.get('local_guardian_qualification')
        local_guardian_qualification_other = request.POST.get('local_guardian_qualification_other')
        Handicapped = request.POST.get('Handicapped')
        caste = request.POST.get('caste')
        caste_id = request.POST.get('caste_id')
        nationality = request.POST.get('nationality')
        aadhar_no = request.POST.get('aadhar_no')
        religion = request.POST.get('religion')
        boarding_for = request.POST.get('boarding_for')
        blood_group = request.POST.get('blood_group')
        date_of_submission = request.POST.get('date_of_submission')

        # Handle 'Others' values
        if mothers_occupation == 'Others':
            mothers_occupation = mothers_occupation_other
        if mothers_qualification == 'Others':
            mothers_qualification = mothers_qualification_other
        if fathers_occupation == 'Others':
            fathers_occupation = fathers_occupation_other
        if fathers_qualification == 'Others':
            fathers_qualification = fathers_qualification_other
        if local_guardian == 'Others':
            local_guardian = local_guardian_other
        if local_guardian_occupation == 'Others':
            local_guardian_occupation = local_guardian_occupation_other
        if local_guardian_qualification == 'Others':
            local_guardian_qualification = local_guardian_qualification_other

        # Create and save the StudentRegistration instance
        student_registration = StudentRegistration(
            name=name, address=address, contact=contact, gender=gender, date_of_birth=date_of_birth,
            class_for=class_for, date_of_entry=date_of_entry, last_school_attended=last_school_attended,
            last_class_attended=last_class_attended, last_examination_attended=last_examination_attended,
            result=result, mothers_name=mothers_name, mothers_occupation=mothers_occupation,
            mothers_qualification=mothers_qualification, mothers_mobile_no=mothers_mobile_no, 
            fathers_name=fathers_name, fathers_occupation=fathers_occupation,
            fathers_qualification=fathers_qualification, fathers_mobile_no=fathers_mobile_no,
            local_guardian=local_guardian, local_guardian_occupation=local_guardian_occupation,
            local_guardian_qualification=local_guardian_qualification, Handicapped=Handicapped, 
            caste=caste, caste_id=caste_id, nationality=nationality, aadhar_no=aadhar_no,
            religion=religion, boarding_for=boarding_for, blood_group=blood_group, 
            date_of_submission=date_of_submission
        )
        student_registration.save()
        messages.success(request, "Student Registered Successfully!")
        return redirect('Student_registration_bill', id=student_registration.id)

    return render(request, 'Admin/student_registration.html', {'class_choices': class_choices})


@admin_required
@other_section_required
def REGISTER_STUDENT_LIST(request):
    student_registration = StudentRegistration.objects.all()
    return render(request,'Admin/student_registration_list.html',{'student_registration':student_registration})


@admin_required
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # Use your Django project's static root for static files
    static_root = os.path.join(os.path.dirname(__file__), 'static')
    if uri.startswith('static/'):
        path = os.path.join(static_root, uri.replace('static/', ''))
    else:
        path = os.path.join(static_root, uri)
    
    # Make sure that file exists
    if not os.path.isfile(path):
        raise Exception(f'media URI must start with static/ or be a valid path, not {uri}')
    return path

@admin_required
def MONTHLY_TRANSPORT_BILL(request,student_id,month):
    student = Student.objects.get(id=student_id)
    transportfee= TransportFee.objects.get(student=student)

    month_lower = month.lower()[:3]  # Convert month name to lowercase 3-letter abbreviation
    month_data = {
        'month': month,
        'amount': transportfee.transport_fees.amount,  # Assuming amount is stored in FeeStructure
        'payment_date': getattr(transportfee, f'{month_lower}_payment_date'),
        'status': getattr(transportfee, f'{month_lower}_status'),
    }
    context = {
        'student': student,
        'transportfee': transportfee,
        'month_data': month_data,
    }
    return render(request,'Admin/monthly_transport_bill.html',context)

@admin_required
@account_section_required
def MONTHLY_FEES_BILL(request, student_id, month):
    student = Student.objects.get(id=student_id)
    fee = Fee.objects.get(student=student)

    # List of month abbreviations
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    # Initialize total dues for all months
    total_due = 0
    total_transport_due = 0
    total_hostel_due = 0

    # Iterate through each month to calculate total dues
    for month_abbr in months:
        total_due += getattr(fee, f'{month_abbr}_due') or 0
        total_transport_due += getattr(fee, f'{month_abbr}_transport_due') or 0
        total_hostel_due += getattr(fee, f'{month_abbr}_hostel_due') or 0

    # Overall total dues for all months
    overall_total_due = total_due + total_transport_due + total_hostel_due

    # Get the specific selected month's data
    month_lower = month.lower()[:3]  # Convert month name to lowercase 3-letter abbreviation
    month_data = {
        'month': month,
        'TuAmount': fee.fee_structure.amount,  # Assuming amount is stored in FeeStructure
        'Hamount': fee.hostelfee.amount,
        'TrAmount': fee.transport_fees.amount,
        'Tdue': overall_total_due,  # Total due for the entire year
        'payment_date': getattr(fee, f'{month_lower}_payment_date'),
        'status': getattr(fee, f'{month_lower}_status'),
    }

    # Calculate the total amount (including the total dues for the entire year)
    month_data['TotalAmount'] = (
        month_data['TuAmount'] + 
        month_data['Hamount'] + 
        month_data['TrAmount'] + 
        month_data['Tdue']
    )

    # Convert the total amount to words
    total_amount_in_words = num2words(
        month_data['TotalAmount'], 
        to='currency', 
        lang='en'
    ).replace('euro', 'rupees').replace('cents', 'paise').upper()

    # Prepare context for the template
    context = {
        'student': student,
        'fee': fee,
        'month_data': month_data,
        'total_amount_in_words': total_amount_in_words,
        'total_due': overall_total_due,  # Add this for displaying total dues in the template
    }

    return render(request, 'Admin/monthly_fees_bill.html', context)

    
@admin_required
@other_section_required
def ADD_STAFF(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        father_name = request.POST.get('father_name')
        sex = request.POST.get('sex')
        date_of_birth = request.POST.get('date_of_birth')
        permanent_address = request.POST.get('permanent_address')
        teaching_subject = request.POST.get('teaching_subject')
        qualification = request.POST.get('qualification')
        contact_number = request.POST.get('contact_number')
        date_of_joining = request.POST.get('date_of_joining')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('add_teacher')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('add_teacher')

        try:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                user_type=2
            )
            user.set_password(password)
            user.save()

            staff = Teacher(
                admin=user,
                father_name=father_name,
                sex=sex,
                date_of_birth=date_of_birth,
                permanent_address=permanent_address,
                teaching_subject=teaching_subject,
                qualification=qualification,
                contact_number=contact_number,
                date_of_joining=date_of_joining,
            )
            staff.save()
            messages.success(request, "Teacher Successfully Added!")
            return redirect('add_teacher')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_teacher')

    return render(request, 'Admin/add_teacher.html')

def ADD_ACCOUNTS(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        accounts = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            user_type=4

        )
        accounts.set_password(password)
        accounts.save()
        messages.success(request, "Accountant Successfully Added!")
        return redirect ('add_accounts')
    return render(request,'Admin/add_accounts.html')

@admin_required
@other_section_required
def LIST_STAFF(request):
    staff = Teacher.objects.all()

    context = {
        'staff':staff
    }
    return render (request,'Admin/view_teacher.html',context)

@admin_required
@other_section_required
def EDIT_TEACHER(request,id):
    teacher = Teacher.objects.filter(id=id)
    return render(request,'Admin/edit_teacher.html',{'teacher':teacher})

@admin_required
@other_section_required
def UPDATE_TEACHER(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(Teacher, id=teacher_id)
        user = teacher.admin

        # Update User model fields
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.username = request.POST.get('username', '').strip()
        user.email = request.POST.get('email', '').strip()

        # Update password if provided
        new_password = request.POST.get('password', '').strip()
        if new_password:
            user.set_password(new_password)

        
            
        user.save()

        teacher.father_name = request.POST.get('father_name')
        teacher.sex = request.POST.get('sex')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.permanent_address = request.POST.get('permanent_address')
        teacher.teaching_subject = request.POST.get('teaching_subject')
        teacher.qualification = request.POST.get('qualification')
        teacher.contact_number = request.POST.get('contact_number')
        teacher.date_of_joining = request.POST.get('date_of_joining')
        teacher.save()
        messages.success(request, "Teacher Successfully Updated!")

        return redirect('list_teacher')
    return render(request,'Admin/edit_teacher.html',{'teacher':teacher})

@admin_required
@other_section_required
def ADD_STUDENT(request):
    class_choices = Student.class_choices
    section_choices = Student.section_choices

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        date_of_birth = request.POST.get('date_of_birth')
        classes = request.POST.get('classes')
        religion = request.POST.get('religion')
        gender = request.POST.get('gender')
        mobile_number = request.POST.get('mobile_number')
        admission_no = request.POST.get('admission_no')
        section = request.POST.get('section')
        profile_pic = request.FILES.get('profile_pic')
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        fathers_occupation_other = request.POST.get('fathers_occupation_other')
        father_mobile_number = request.POST.get('father_mobile_number')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mothers_occupation_other = request.POST.get('mothers_occupation_other')
        mother_mobile_number = request.POST.get('mother_mobile_number')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        fee_structure_id = request.POST.get('fee_structure')
        transport_fees_id = request.POST.get('transport_fees')
        hostelfee_id = request.POST.get('hostelfee')
        roll_no = request.POST.get('roll_no')
        student_type = request.POST.get('student_type')
        country = request.POST.get('country')

        print(f"Mother Occupation: {mother_occupation}")
        print(f"Mother's Other Occupation: {mothers_occupation_other}")

        

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists!")
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists!")
            return redirect('add_student')
        
        try:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()
            
            if father_occupation == 'Others':
                father_occupation = fathers_occupation_other
            if mother_occupation == 'Others':
                mother_occupation = mothers_occupation_other
            print(f"Final Mother Occupation: {mother_occupation}")


            student = Student(
                admin=user,
                classes=classes,
                religion=religion,
                gender=gender,
                student_id=student_id,
                date_of_birth=date_of_birth,
                mobile_number=mobile_number,
                admission_no=admission_no,
                section=section,
                father_name=father_name,
                father_occupation=father_occupation,
                father_mobile_number=father_mobile_number,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                mother_mobile_number=mother_mobile_number,
                present_address=present_address,
                permanent_address=permanent_address,
                roll_no = roll_no,
                student_type = student_type,
                country = country ,
            )
            student.save()
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_student')
        messages.success(request, "Student added successfully!")
        
        try:
            fee_structure = FeeStructure.objects.get(id=fee_structure_id)
            transport_fees = Transport_Fees.objects.get(id=transport_fees_id)
            hostelfee = HostelFee.objects.get(id=hostelfee_id)
            
            fee = Fee(
                student=student,
                fee_structure=fee_structure,
                transport_fees=transport_fees,
                hostelfee=hostelfee
            )
            fee.save()
        except FeeStructure.DoesNotExist:
            messages.warning(request, "Invalid fee structure selected!")
            return redirect('add_student')
        except Transport_Fees.DoesNotExist:
            messages.warning(request, "Invalid transport fee selected!")
            return redirect('add_student')
        except HostelFee.DoesNotExist:
            messages.warning(request, "Invalid hostel fee selected!")
            return redirect('add_student')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_student')

        messages.success(request, "Student and fee information added successfully!")
        return redirect('add_student')

    fee_structures = FeeStructure.objects.all()
    transports = Transport_Fees.objects.all()
    hostelfees = HostelFee.objects.all()

    return render(request, 'Admin/add_student.html', {
        'fee_structures': fee_structures,
        'transports': transports,
        'hostelfees': hostelfees,
        'class_choices': class_choices,
        'section_choices': section_choices
    })

@admin_required
@student_section_required
def LIST_STUDENT(request):
    form = ClassFilterForm(request.GET)
    student = Student.objects.all()
    
    if form.is_valid():
        class_filter = form.cleaned_data.get('class_filter')
        if class_filter:
            student = student.filter(classes=class_filter)
    
    context = {
        'student': student,
        'form': form,
    }  


    return render(request,'Admin/view_student.html',context)

@admin_required
@other_section_required
def VIEW_STUDENT(request,id):
    student = Student.objects.filter(id=id)

    context = { 
        'student':student,
        }
    return render(request,'Admin/student_view.html',context)

@admin_required
@other_section_required
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id=id)
    fee_structures = FeeStructure.objects.all()
    fee = Fee.objects.filter(id=id)
    transports = Transport_Fees.objects.all()
    class_choices = Student.class_choices
    section_choices = Student.section_choices
    

    context = {
        'student':student,
        'fee_structures':fee_structures,
        'transports':transports,
        'fee':fee,
        'class_choices':class_choices,
        'section_choices':section_choices,

    }
    return render (request,'Admin/edit_student.html',context)

@admin_required
@other_section_required
def UPDATE_STUDENT(request):
    if request.method == 'POST':
        st_id = request.POST.get('st_id')
        student = get_object_or_404(Student, id=st_id)
        user = student.admin

        # Update User model fields
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.username = request.POST.get('username', '').strip()
        user.email = request.POST.get('email', '').strip()

        # Update password if provided
        new_password = request.POST.get('password', '').strip()
        if new_password:
            user.set_password(new_password)

        # Update profile picture if provided
        if 'profile_pic' in request.FILES:
            if user.profile_pic:
                # Delete the old profile picture file
                user.profile_pic.delete(save=False)
            user.profile_pic = request.FILES['profile_pic']
        user.save()

        # Update Student model fields
        student.student_id = request.POST.get('student_id', '').strip()
        student.gender = request.POST.get('gender', '').strip()
        student.classes = request.POST.get('classes', '').strip()
        student.section = request.POST.get('section', '').strip()
        student.roll_no = request.POST.get('roll_no', '').strip()
        student.religion = request.POST.get('religion', '').strip()
        student.date_of_birth = request.POST.get('date_of_birth', '').strip()
        student.mobile_number = request.POST.get('mobile_number', '').strip()
        student.admission_no = request.POST.get('admission_no', '').strip()
        student.father_name = request.POST.get('father_name', '').strip()
        student.father_occupation = request.POST.get('father_occupation', '').strip()
        student.father_mobile_number = request.POST.get('father_mobile_number', '').strip()
        student.mother_name = request.POST.get('mother_name', '').strip()
        student.mother_occupation = request.POST.get('mother_occupation', '').strip()
        student.mother_mobile_number = request.POST.get('mother_mobile_number', '').strip()
        student.present_address = request.POST.get('present_address', '').strip()
        student.permanent_address = request.POST.get('permanent_address', '').strip()
        student.student_type = request.POST.get('student_type', '').strip()
        student.country = request.POST.get('country', '').strip()

        student.save()
        messages.success(request, 'Student Successfully Updated!')

        # Update Fee structure
        fee_structure_id = request.POST.get('fee_structure')
        try:
            fee_structure = FeeStructure.objects.get(id=fee_structure_id)
            fee, created = Fee.objects.get_or_create(student=student)
            fee.fee_structure = fee_structure
            fee.save()
        except (FeeStructure.DoesNotExist, ValueError):
            messages.warning(request, "Invalid fee structure selected!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.success(request, 'Student Successfully Updated!')
        
        return redirect('list_student')

    # If the request is not POST, redirect back to the edit page
    st_id = request.GET.get('st_id')
    return redirect('edit_student', id=st_id)

@admin_required
@other_section_required
def DELETE_STUDENT(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        Fee.objects.filter(student=student).delete()
        StudentResult.objects.filter(student= student).delete()
        Attendance.objects.filter(student=student).delete()
        
        user = student.admin  

        
        student.delete()
        user.delete()

        messages.success(request, "Student deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('list_student')  

    
@admin_required
@account_section_required
def FEES_COLLECTION(request):
    form = ClassFilterForm(request.GET)
    students = Student.objects.all()
    
    if form.is_valid():
        class_filter = form.cleaned_data.get('class_filter')
        if class_filter:
            students = students.filter(classes=class_filter)
    
    context = {
        'students': students,
        'form': form,
    }
    return render(request, 'Admin/fees_collection.html', context)


from decimal import Decimal, InvalidOperation
@login_required
@admin_required
@account_section_required
def UPDATE_FEES(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    fee_structure = FeeStructure.objects.get(class_name=student.classes)
    fees, created = Fee.objects.get_or_create(student=student, defaults={'fee_structure': fee_structure})
    
    months = [
        ('jan', 'January'), ('feb', 'February'), ('mar', 'March'),
        ('apr', 'April'), ('may', 'May'), ('jun', 'June'),
        ('jul', 'July'), ('aug', 'August'), ('sep', 'September'),
        ('oct', 'October'), ('nov', 'November'), ('dec', 'December')
    ]
    
    if request.method == 'POST':
        for month, _ in months:
            payment_date_str = request.POST.get(f'{month}_payment_date')
            status = request.POST.get(f'{month}_status')
            due_str = request.POST.get(f'{month}_due')
            trans_str = request.POST.get(f'{month}_transport_due')
            hostel_str = request.POST.get(f'{month}_hostel_due')
            
            # Only update fields if they are provided in the POST data
            if payment_date_str:
                try:
                    payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d').date()
                    setattr(fees, f'{month}_payment_date', payment_date)
                except ValueError:
                    messages.error(request, f'Invalid date format for {month.capitalize()}. Please use YYYY-MM-DD.')
                    return redirect('update_fees', student_id=student_id)
            
            if status:
                setattr(fees, f'{month}_status', status)
            
            if due_str:
                try:
                    due = Decimal(due_str)
                    setattr(fees, f'{month}_due', due)
                except InvalidOperation:
                    messages.error(request, f'Invalid amount format for {month.capitalize()} tuition due. Please use valid decimal numbers.')
                    return redirect('update_fees', student_id=student_id)
            
            if trans_str:
                try:
                    trans = Decimal(trans_str)
                    setattr(fees, f'{month}_transport_due', trans)
                except InvalidOperation:
                    messages.error(request, f'Invalid amount format for {month.capitalize()} transport due. Please use valid decimal numbers.')
                    return redirect('update_fees', student_id=student_id)
            
            if hostel_str:
                try:
                    hostel = Decimal(hostel_str)
                    setattr(fees, f'{month}_hostel_due', hostel)
                except InvalidOperation:
                    messages.error(request, f'Invalid amount format for {month.capitalize()} hostel due. Please use valid decimal numbers.')
                    return redirect('update_fees', student_id=student_id)
        
        fees.save()
        messages.success(request, "Fees updated successfully!")
        return redirect('update_fees', student_id=student_id)
    
    context = {
        'student': student,
        'fees': fees,
        'months': months,
    }
   
    return render(request, 'Admin/payment_update.html', context)



from django.shortcuts import get_object_or_404, redirect

# You can create these records when a student is created
@admin_required
@account_section_required
def TRANSPORT(request):
    students = Student.objects.all()
    filter_form = StudentFilterForm(request.GET or None)
    
    if filter_form.is_valid():
        class_name = filter_form.cleaned_data['class_name']
        section = filter_form.cleaned_data['section']
        
        if class_name and section:
            students = students.filter(classes=class_name, section=section)
    
    context = {
        'students': students,
        'filter_form': filter_form,
    }
    return render(request, 'Admin/transport.html', context)


@admin_required
@account_section_required
def ADD_FEE_STRUCTURE(request):
    class_choices = Student.class_choices

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        amount = request.POST.get('amount')

        if FeeStructure.objects.filter(class_name=class_name).exists():
            messages.warning(request,"Class already exists !")
            return redirect('add_fees_structure')
        else:
            fees=FeeStructure(
                class_name = class_name,
                amount = amount,
            )
            fees.save()
            messages.success(request,"Fees Structure Successfully Added !")
            return redirect('add_fees_structure')
    
    return render(request,'Admin/add_fee_structure.html',{'class_choices':class_choices,})

@admin_required
def VIEW_FEE_STRUCTURE(request):
    fee_structure = FeeStructure.objects.all()
    
    return render(request,'Admin/view_fee_structure.html',{'fee_structure':fee_structure})

@admin_required
@other_section_required
def SEND_NOTICE(request):
    if request.method == 'POST':
        types = request.POST.get('types')
        title = request.POST.get('title')
        sent_by = request.POST.get('sent_by')
        message = request.POST.get('message')

        notice = Notice(
            types = types,
            title = title,
            sent_by = sent_by,
            message = message,

        )
        notice.save()
        messages.success(request,"Notice Successfully Sent !")
        return redirect('student_send_notification')

@admin_required
@other_section_required
def STUDENT_SEND_NOTIFICATION(request):
    class_choices= Student.class_choices
    notification = Student_Notification.objects.all().order_by('-sent_at')[:5]
    notice = Notice.objects.all().order_by('-created_at')[:5]

    
    if request.method =="POST":
        class_name = request.POST.get('class_name')
        message = request.POST.get('message')
        sent_by = request.POST.get('sent_by')

        student_notification=Student_Notification(
            class_name = class_name,
            message = message,
            sent_by = sent_by,
        )
        student_notification.save()
        messages.success(request,"Notification Successfully Sent !")
        return redirect('student_send_notification')
    

    return render(request,"Admin/student_notification.html",{'notification':notification,'class_choices':class_choices,
                                                             'notice':notice})


# from datetime import date
# from django.db.models import Count, Case, When, IntegerField

# @login_required(login_url='/')
# def ADMIN_ATTENDANCE_VIEW(request):
#     form = AttendanceFilterForm(request.GET or None)
#     attendance_summary = []

#     if form.is_valid():
#         class_name = form.cleaned_data.get('class_name')
#         section_name = form.cleaned_data.get('section_name')
#         start_date = form.cleaned_data.get('start_date')
#         end_date = form.cleaned_data.get('end_date') or date.today()

#         if class_name and section_name and start_date:
#             students = Student.objects.filter(classes=class_name, section=section_name)
            
#             for student in students:
#                 attendances = Attendance.objects.filter(
#                     student=student,
#                     date__range=[start_date, end_date]
#                 ).order_by('date')
                
#                 attendance_details = []
#                 for attendance in attendances:
#                     attendance_details.append({
#                         'id': attendance.id,
#                         'date': attendance.date,
#                         'status': attendance.status
#                     })
                
#                 total_days = attendances.count()
#                 present_days = attendances.filter(status='present').count()
                
#                 if total_days > 0:
#                     attendance_summary.append({
#                         'student_id': student.id,
#                         'student_name': f"{student.admin.first_name} {student.admin.last_name}",
#                         'class': student.classes,
#                         'section': student.section,
#                         'present_days': present_days,
#                         'total_days': total_days,
#                         'ratio': f"{present_days}/{total_days}",
#                         'attendance_details': attendance_details
#                     })

#     context = {
#         'form': form,
#         'attendance_summary': attendance_summary,
#     }

#     return render(request, 'Admin/view_attendance.html', context)


# @login_required(login_url='/')
# def EDIT_ATTENDANCE(request):
#     if request.method == "POST":
#         attendance_id = request.POST.get('attendance_id')
#         new_status = request.POST.get('status')
        
#         try:
#             attendance = Attendance.objects.get(id=attendance_id)
#             attendance.status = new_status
#             attendance.save()
#             messages.success(request, f"{attendance.student.admin.first_name} {attendance.student.admin.last_name} updated successfully!")
#         except Attendance.DoesNotExist:
#             messages.error(request, "Attendance record not found.")
        
#     return redirect('admin_view_attendance')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Case, When, IntegerField
from datetime import date

@login_required(login_url='/')
def ADMIN_ATTENDANCE_VIEW(request):
    form = AttendanceFilterForm(request.GET or None)
    attendance_summary = []
    edit_date = request.GET.get('edit_date')
    edit_class = request.GET.get('edit_class')
    edit_section = request.GET.get('edit_section')

    if form.is_valid():
        class_name = form.cleaned_data.get('class_name')
        section_name = form.cleaned_data.get('section_name')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date') or date.today()

        if class_name and section_name and start_date:
            students = Student.objects.filter(classes=class_name, section=section_name)
            
            for student in students:
                attendances = Attendance.objects.filter(
                    student=student,
                    date__range=[start_date, end_date]
                ).order_by('date')
                
                total_days = attendances.count()
                present_days = attendances.filter(status='present').count()
                
                if total_days > 0:
                    attendance_summary.append({
                        'student_id': student.id,
                        'student_name': f"{student.admin.first_name} {student.admin.last_name}",
                        'class': student.classes,
                        'section': student.section,
                        'present_days': present_days,
                        'total_days': total_days,
                        'ratio': f"{present_days}/{total_days}",
                    })

    if edit_date and edit_class and edit_section:
        return redirect('edit_attendance', date=edit_date, class_name=edit_class, section=edit_section)

    context = {
        'form': form,
        'attendance_summary': attendance_summary,
        'class_choices': Student.class_choices,
        'section_choices': Student.section_choices,
    }

    return render(request, 'Admin/view_attendance.html', context)

@login_required(login_url='/')
def EDIT_ATTENDANCE(request, date, class_name, section):
    if request.method == "POST":
        students = Student.objects.filter(classes=class_name, section=section)
        for student in students:
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=date,
                defaults={'status': 'absent'}
            )
            new_status = 'present' if request.POST.get(f'student_{student.id}') else 'absent'
            attendance.status = new_status
            attendance.save()
        
        messages.success(request, f"Attendance for {date} updated successfully!")
        return redirect('admin_view_attendance')

    students = Student.objects.filter(classes=class_name, section=section)
    attendances = Attendance.objects.filter(student__in=students, date=date)
    
    attendance_data = []
    for student in students:
        attendance = attendances.filter(student=student).first()
        attendance_data.append({
            'student_id': student.id,
            'student_name': f"{student.admin.first_name} {student.admin.last_name}",
            'status': attendance.status if attendance else 'absent'
        })

    context = {
        'date': date,
        'class_name': class_name,
        'section': section,
        'attendance_data': attendance_data,
    }

    return render(request, 'Admin/edit_attendance.html', context)

@admin_required
def ADD_ITEMS(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        product = Product(
            name=name, price=price, stock=stock, image=image)
        product.save()
        messages.success(request,"Items Successfully Added to Library !")
        return redirect('library')
    
    return render(request, 'Admin/add_items.html')
from .forms import ProductForm

@admin_required
def update_delete(request):
    products = Product.objects.all()  # Fetch all products

    if request.method == 'POST':
        product_id = request.POST.get('product_id')  # Get the product ID from the form
        product = get_object_or_404(Product, id=product_id)

        if 'update' in request.POST:
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('library')  # Redirect to the library or another page
        elif 'delete' in request.POST:
            product.delete()
            return redirect('library')  # Redirect after deletion

    return render(request, 'Admin/update_delete.html', {'products': products})
# Edit the product 
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST,  request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('library')  # Redirect to the library after updating
    else:
        form = ProductForm(instance=product)

    return render(request, 'Admin/edit_product.html', {'form': form, 'product': product})

@admin_required
def LIBRARY(request):      

    product = Product.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items_count = CartItem.objects.filter(cart=cart).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    context={
        'product':product,
        'cart_items_count':cart_items_count,
    }


    return render(request,'Admin/library.html',context) 

@admin_required
def CHECKOUT(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Get all unique class choices from the Student model
    classes = [choice[0] for choice in Student.class_choices]
    
    students = None  # Initialize students
    bill_details = None

    if request.method == 'POST':
        selected_class = request.POST.get('class_id', None)
        search_query = request.POST.get('search_query', '').strip()

        # Filter students based on selected class and search query
        if selected_class:  # Ensure a class is selected
            students = Student.objects.filter(classes=selected_class)

            # If there is a search query, apply it to filter students further by their admin's first name
            if search_query:
                students = students.filter(admin__first_name__icontains=search_query)

        if request.POST.get('generate_bill'):
            selected_student_id = request.POST.get('selected_student', None)
            if selected_student_id:
                return redirect('generate_bill', user_id=selected_student_id)
        
    return render(request, 'Admin/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'all_classes': classes,  # Adjusted to match your variable naming
        'students': students,
        'bill_details': bill_details,
    })





@admin_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:  # If the item already exists, just increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    # If the item was newly created, the quantity is already set to 1 by default
    
    return redirect('library')  # Redirect to the page where the products are listed
@admin_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.cart.user == request.user:
        cart_item.delete()
    return redirect('checkout')

@admin_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('checkout')  # Adjust this URL to your cart page

@admin_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Optionally handle removal if quantity is 1
        cart_item.delete()
    return redirect('checkout') 



# Choose Student logic for the bill 
from django.shortcuts import render, redirect, get_object_or_404
# from models import Student, Cart, CartItem

@admin_required
def choose_student(request):
    # Get all unique class choices from the Student model
    all_classes = Student.class_choices  # Assuming class_choices is a list of tuples
    print(all_classes)
    students = None  # Placeholder for students to be displayed

    if request.method == 'POST':
        selected_class = request.POST.get('class_id', None)
        search_query = request.POST.get('search_query', '').strip()

        # Filter students based on selected class and search query
        if selected_class:  # Ensure a class is selected
            students = Student.objects.filter(classes__name=selected_class)

            # If there is a search query, apply it to filter students further by their admin's first name
            if search_query:
                students = students.filter(admin__first_name__icontains=search_query)

    return render(request, 'Admin/checkout.html', {
        'all_classes': all_classes,  # Pass the list of classes to the template
        'students': students,
    })



@admin_required
def generate_bill(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, id=student_id)

        # Fetch the user's cart
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Initialize total price and student details
        total_price = 0
        student_details = []

        # Process each cart item
        for item in cart_items:
            product = item.product
            
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
                total_price += product.price * item.quantity
                
                # Collect student details
                student_details.append({
                    'roll_no': student.roll_no,
                    'name': f"{student.admin.first_name} {student.admin.last_name}",
                    'mobile_number': student.mobile_number,
                    'product_name': product.name,
                    'quantity': item.quantity,
                    'price': product.price,
                    'total': product.price * item.quantity
                })
                # print(student_details[1])

            item.delete()  # Remove item from cart after processing
        
        # Prepare the bill details
        bill_details = {
            'items': cart_items,  # This will be empty now since items are deleted
            'total_price': total_price,
            'students': student_details
        }
        
        return render(request, 'Admin/generate_bill.html', {
            'total_price': total_price,
            'bill_details': bill_details,
            'student': student
        })

    return redirect('choose_student')  # Redirect if not POST request


def cart(request):
    cart = Cart.objects.get(user=request.user, is_active=True)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})

def checkout(request):
    cart = Cart.objects.get(user=request.user, is_active=True)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart_items:
            item.product.stock -= item.quantity
            item.product.save()
        cart.is_active = False
        cart.save()
        return render(request, 'order_confirmation.html', {'order': order})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@admin_required
@other_section_required
def ADMIN_RESULT_VIEW(request):
    form = StudentFilterForm(request.GET or None)
    students = Student.objects.all()
    results = []

    if form.is_valid():
        class_name = form.cleaned_data.get('class_name')
        section = form.cleaned_data.get('section')

        if class_name and section:
            students = students.filter(classes=class_name, section=section)
            results = StudentResult.objects.filter(student__classes=class_name, student__section=section)

    context = {
        'form': form,
        'students': students,
        'results': results,
    }

    return render(request, 'Admin/view_result.html', context)

@admin_required
@other_section_required
def EDIT_RESULT(request, result_id):
    result = get_object_or_404(StudentResult, id=result_id)
    
    if request.method == "POST":
        first_term_marks = request.POST.get('first_term_marks', result.first_term_marks)
        second_term_marks = request.POST.get('second_term_marks', result.second_term_marks)
        FA_I = request.POST.get('FA_I', result.FA_I)
        NB_I = request.POST.get('NB_I', result.NB_I)
        SE_I = request.POST.get('SE_I', result.SE_I)
        FA_II = request.POST.get('FA_II', result.FA_II)
        NB_II = request.POST.get('NB_II', result.NB_II)
        SE_II = request.POST.get('SE_II', result.SE_II)

        result.first_term_marks = first_term_marks
        result.second_term_marks = second_term_marks
        result.FA_I = FA_I
        result.NB_I = NB_I
        result.SE_I = SE_I
        result.FA_II = FA_II
        result.NB_II = NB_II
        result.SE_II = SE_II

        result.save()
        return redirect('admin_view_result')

    return render(request, 'Admin/edit_result.html', {'result': result})
@admin_required
def ADD_TRANSPORT_FEE(request):
    if request.method == "POST":
        root_name = request.POST.get('root_name')
        amount = request.POST.get('amount')
        
        transport_fee = Transport_Fees(root_name=root_name,amount=amount)
        transport_fee.save()
        messages.success(request,'Added successfully !')
        return redirect('add_transport_fee')
    return render(request, 'Admin/add_transport_fee.html')
    
@admin_required
def DELETE_TRANSPORT_FEE(request,id):
    tranport_fee =Transport_Fees.objects.get(id=id)
    tranport_fee.delete()
    messages.success(request,'Deleted successfully !')
    return redirect('view_transport_fee')





@admin_required
def EDIT_STUDENT_TRANSPORT(request, id):
    student = Student.objects.get(id=id)
    try:
        fee = Fee.objects.get(student=student)
    except Fee.DoesNotExist:
        fee = None

    transport_fees = Transport_Fees.objects.all()
    bus_choices = Fee.BUS_CHOICES

    if request.method == 'POST':
        bus_name = request.POST.get('bus_name')
        transport_fee_id = request.POST.get('transport_fee')

        if fee:
            fee.bus_name = bus_name
            fee.transport_fees_id = transport_fee_id
            fee.save()
        else:
            fee = Fee(
                student=student,
                bus_name=bus_name,
                transport_fees_id=transport_fee_id,
            )
            fee.save()

        messages.success(request, "Transport fee details updated successfully!")
        return redirect('edit_transport_fee', id=id)

    context = {
        'student': student,
        'fee': fee,
        'transport_fees': transport_fees,
        'bus_choices': bus_choices,
    }

    return render(request, "Admin/edit_student_transport.html", context)

@admin_required
def VIEW_TRANSPORT_FEES(request):
    transport_fees = Transport_Fees.objects.all()
    return render(request, 'Admin/view_transport_fee.html',{'transport_fees':transport_fees})


@admin_required
@account_section_required
def ACCOUNTS_HOME(request):
    if not request.session.get('account_section_authenticated'):
        return redirect('account_section_login')
    return render(request, 'Admin/accounts_home.html')

@admin_required
@account_section_required
def ADD_HOSTEL_FEE(request):
    class_choices = Student.class_choices
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        amount = request.POST.get('amount')

        if HostelFee.objects.filter(class_name=class_name).exists():
            messages.warning(request, "Hostel fee for this class already exists!")
            return redirect('add_hostel_fee')

        try:
            hostel_fee = HostelFee(class_name=class_name, amount=amount)
            hostel_fee.save()
            messages.success(request, "Hostel fee details added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_hostel_fee')

    return render(request, 'Admin/add_hostel_fee.html', {'class_choices': class_choices})

@admin_required
@account_section_required
def HOSTEL(request):
    students = Student.objects.all()
    filter_form = StudentFilterForm(request.GET or None)
    
    if filter_form.is_valid():
        class_name = filter_form.cleaned_data['class_name']
        section = filter_form.cleaned_data['section']
        
        if class_name and section:
            students = students.filter(classes=class_name, section=section)
    
    context = {
        'students': students,
        'filter_form': filter_form,
    }
    hostel_fees = HostelFee.objects.all()
    return render(request, 'Admin/hostel.html',context)

@admin_required
@account_section_required
def EDIT_STUDENT_HOSTEL(request, id):
    student = Student.objects.get(id=id)
    try:
        fee = Fee.objects.get(student=student)
    except Fee.DoesNotExist:
        fee = None

    hostel_fees = HostelFee.objects.all()
    bus_choices = Fee.BUS_CHOICES

    if request.method == 'POST':
        # bus_name = request.POST.get('bus_name')
        hostelfee_id = request.POST.get('hostelfee')

        if fee:
            # fee.bus_name = bus_name
            fee.hostelfee_id = hostelfee_id
            fee.save()
        else:
            fee = Fee(
                student=student,
                # bus_name=bus_name,
                hostelfee_id=hostelfee_id,
            )
            fee.save()

        messages.success(request, "Hostel fee details updated successfully!")
        return redirect('edit_hostel_fee', id=id)

    context = {
        'student': student,
        'fee': fee,
        'hostel_fees': hostel_fees,
        'bus_choices': bus_choices,
    }

    return render(request, "Admin/edit_student_hostel.html", context)

@admin_required
@other_section_required
def RESULT(request):
    return render (request,'Admin/result.html')

@admin_required
@other_section_required
def GENERATE_MARKSHEET(request):
    session = MarkSheetSession.objects.first()
    form = StudentFilterForm(request.GET or None)
    students = Student.objects.all()

    # results = []
     # Handle session update
    if request.method == 'POST':
        report_card1 = request.POST.get('report_card1')
        report_card2 = request.POST.get('report_card2')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if session:
            session.report_card1 = report_card1
            session.report_card2 = report_card2
            session.start_date = start_date
            session.end_date = end_date
            session.save()
            messages.success(request, 'Session Updated Successfully')
        else:
            MarkSheetSession.objects.create(
                
                report_card1=report_card1,
                report_card2=report_card2,

                start_date=start_date,
                end_date=end_date
            )
            messages.success(request, 'New Session Created Successfully')

        return redirect('marksheet')

    if form.is_valid():
        class_name = form.cleaned_data.get('class_name')
        section = form.cleaned_data.get('section')

        if class_name and section:
            students = students.filter(classes=class_name, section=section)
            # results = StudentResult.objects.filter(student__classes=class_name, student__section=section)

    context = {
        'form': form,
        'students': students,
        # 'results': results,
    }
    # student = Student.objects.all()
    # result = StudentResult.objects.all()
    return render(request, 'Admin/generate_marksheet.html',context)


@admin_required
@other_section_required
def GENERATE_ADMIT(request):
    session = Session.objects.first()  # Assuming you're working with a single session
    form = StudentFilterForm(request.GET or None)
    students = Student.objects.all()

    # Handle session update
    if request.method == 'POST':
        session_name = request.POST.get('session_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if session:
            session.session_name = session_name
            session.start_date = start_date
            session.end_date = end_date
            session.save()
            messages.success(request, 'Session Updated Successfully')
        else:
            Session.objects.create(
                session_name=session_name,
                start_date=start_date,
                end_date=end_date
            )
            messages.success(request, 'New Session Created Successfully')

        return redirect('generate_admit')

    # Handle student filtering
    if form.is_valid():
        class_name = form.cleaned_data.get('class_name')
        section = form.cleaned_data.get('section')
        if class_name and section:
            students = students.filter(classes=class_name, section=section)

    # Handle print all
    if 'print_all' in request.GET:
        student_ids = students.values_list('id', flat=True)
        return redirect('print_admit', student_ids=','.join(map(str, student_ids)))

    context = {
        'form': form,
        'students': students,
        'session': session,
    }
    return render(request, 'Admin/generate_admit.html', context)

@admin_required
@other_section_required
def PRINT_ADMIT(request, student_ids):
    session = Session.objects.all()
    student_ids = list(map(int, student_ids.split(',')))
    students = Student.objects.filter(id__in=student_ids)
    
    all_students_data = []
    for student in students:
        routine = Routine.objects.filter(class_name=student.classes)
        all_students_data.append({
            'student': student,
            'routine': routine
        })
    
    context = {
        'all_students_data': all_students_data,
        'session': session,
    }
    
    return render(request, 'Admin/print_admit.html', context)


@admin_required
@other_section_required
def PRINT_MARKSHEET(request, student_id):
    session=MarkSheetSession.objects.all()
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.filter(class_name=student.classes)
    results = StudentResult.objects.filter(student=student)
    
    # Calculate attendance
    current_year = date.today().year
    total_school_days = Attendance.objects.filter(
        date__year=current_year,
        student__classes=student.classes
    ).count()
    
    student_attendance = Attendance.objects.filter(
        student=student,
        date__year=current_year,
        status='present'
    ).count()
    
    # Calculate marks and grades
    subject_results = []
    total_marks = 0
    total_possible_marks = 0
    grand_total = 0
    total_first_term =0
    total_second_term =0
    
    for subject in subjects:
        result = results.filter(subject=subject).first()
        if result:
            first_total = result.FA_I + result.NB_I + result.SE_I + result.first_term_marks
            second_total = result.FA_II + result.NB_II + result.SE_II + result.second_term_marks
            annual_total = first_total + second_total
            percentage = (annual_total / 200) * 100
            
            subject_results.append({
                'subject': subject.subject_name,
                'FA_I': result.FA_I,
                'NB_I': result.NB_I,
                'SE_I': result.SE_I,
                'TERM_I': result.first_term_marks,
                'Total_I': first_total,
                'GR_I': get_grade(first_total),
                'FA_II': result.FA_II,
                'NB_II': result.NB_II,
                'SE_II': result.SE_II,
                'TERM_II': result.second_term_marks,
                'Total_II': second_total,
                'GR_II': get_grade(second_total),
                'TOTAL_I_II': annual_total,
                
                'PER': round(percentage, 2),
                'Grade': get_grade(percentage)
            })
            total_first_term += first_total
            total_second_term += second_total
            total_marks += annual_total
            total_possible_marks += 100  # Assuming each subject is out of 200
            grand_total += annual_total
    
    overall_percentage = (total_marks / total_possible_marks) * 100 if total_possible_marks > 0 else 0
    overall_grade = get_grade(overall_percentage)
    remarks = get_remarks(overall_percentage)
    
    # Calculate rank (if needed)
    # This is a simple implementation and might need to be adjusted based on your specific ranking criteria
    all_students = Student.objects.filter(classes=student.classes)
    student_ranks = []
    for s in all_students:
        s_results = StudentResult.objects.filter(student=s)
        s_total = sum(r.first_term_marks + r.second_term_marks for r in s_results)
        student_ranks.append((s, s_total))
    
    student_ranks.sort(key=lambda x: x[1], reverse=True)
    rank = next(i for i, (s, _) in enumerate(student_ranks, 1) if s == student) if student in [s for s, _ in student_ranks] else '-'
    
    context = {
        'student': student,
        'subject_results': subject_results,
        'total_marks': total_marks,
        'total_possible_marks': total_possible_marks,
        'overall_percentage': round(overall_percentage, 2),
        'overall_grade': overall_grade,
        'remarks': remarks,
        'attendance': student_attendance,
        'total_school_days': total_school_days,
        'rank': rank,
        'total_FA_I': sum(result.FA_I for result in results),
        'total_FA_II': sum(result.FA_II for result in results),
        'total_TERM_I':sum(result.first_term_marks for result in results),
        'total_TERM_II':sum(result.second_term_marks for result in results),
        'grand_total': grand_total,
        'total_first_term': total_first_term,
        'total_second_term': total_second_term,
        'session':session,

    }
    
    return render(request, 'Admin/marksheet.html', context)

@admin_required
@other_section_required
def PRINT_MARKSHEET_1(request,student_id):
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.filter(class_name=student.classes)
    results = StudentResult.objects.filter(student=student)
    
    # Calculate attendance
    current_year = date.today().year
    total_school_days = Attendance.objects.filter(
        date__year=current_year,
        student__classes=student.classes
    ).count()
    
    student_attendance = Attendance.objects.filter(
        student=student,
        date__year=current_year,
        status='present'
    ).count()
    
    # Calculate marks and grades
    subject_results = []
    total_marks = 0
    total_possible_marks = 0
    grand_total = 0
    total_first_term =0
    total_second_term =0
    
    for subject in subjects:
        result = results.filter(subject=subject).first()
        if result:
            first_total = result.FA_I + result.NB_I + result.SE_I + result.first_term_marks
            second_total = result.FA_II + result.NB_II + result.SE_II + result.second_term_marks
            annual_total = first_total + second_total
            percentage = (annual_total / 200) * 100
            
            subject_results.append({
                'subject': subject.subject_name,
                'FA_I': result.FA_I,
                'NB_I': result.NB_I,
                'SE_I': result.SE_I,
                'TERM_I': result.first_term_marks,
                'Total_I': first_total,
                'GR_I': get_grade(first_total),
                'FA_II': result.FA_II,
                'NB_II': result.NB_II,
                'SE_II': result.SE_II,
                'TERM_II': result.second_term_marks,
                'Total_II': second_total,
                'GR_II': get_grade(second_total),
                'TOTAL_I_II': annual_total,
                
                'PER': round(percentage, 2),
                'Grade': get_grade(percentage)
            })
            total_first_term += first_total
            total_second_term += second_total
            total_marks += annual_total
            total_possible_marks += 200  # Assuming each subject is out of 200
            grand_total += annual_total
    
    overall_percentage = (total_marks / total_possible_marks) * 100 if total_possible_marks > 0 else 0
    overall_grade = get_grade(overall_percentage)
    remarks = get_remarks(overall_percentage)
    
    # Calculate rank (if needed)
    # This is a simple implementation and might need to be adjusted based on your specific ranking criteria
    all_students = Student.objects.filter(classes=student.classes)
    student_ranks = []
    for s in all_students:
        s_results = StudentResult.objects.filter(student=s)
        s_total = sum(r.first_term_marks + r.second_term_marks for r in s_results)
        student_ranks.append((s, s_total))
    
    student_ranks.sort(key=lambda x: x[1], reverse=True)
    rank = next(i for i, (s, _) in enumerate(student_ranks, 1) if s == student) if student in [s for s, _ in student_ranks] else '-'
    
    context = {
        'student': student,
        'subject_results': subject_results,
        'total_marks': total_marks,
        'total_possible_marks': total_possible_marks,
        'overall_percentage': round(overall_percentage, 2),
        'overall_grade': overall_grade,
        'remarks': remarks,
        'attendance': student_attendance,
        'total_school_days': total_school_days,
        'rank': rank,
        'total_FA_I': sum(result.FA_I for result in results),
        'total_FA_II': sum(result.FA_II for result in results),
        'total_TERM_I':sum(result.first_term_marks for result in results),
        'total_TERM_II':sum(result.second_term_marks for result in results),
        'grand_total': grand_total,
        'total_first_term': total_first_term,
        'total_second_term': total_second_term,
    }
        


    return render(request, 'Admin/marksheet_1.html',context)

    
    

def get_grade(percentage):
    if percentage >= 91: return 'A1'
    elif percentage >= 81: return 'A2'
    elif percentage >= 71: return 'B1'
    elif percentage >= 61: return 'B2'
    elif percentage >= 51: return 'C1'
    elif percentage >= 41: return 'C2'
    else: return 'D'
    

def get_remarks(percentage):
    if percentage >= 80: return 'Excellent'
    elif percentage >= 60: return 'Good'
    elif percentage >= 40: return 'Fair'
    else: return 'Poor'

def SUBJECT_VIEW(request):
    subject = Subject.objects.all()
    form = ClassFilterForm(request.GET)
    
    
    if form.is_valid():
        class_filter = form.cleaned_data.get('class_filter')
        if class_filter:
            subject = subject.filter(class_name=class_filter)
    
    return render(request, 'Admin/subject_view.html',{'subject':subject,'form':form,})
   
def add_notifications(request):
    
    return render (request,'Admin/add_notification.html')

def ShowFeedback(request):
    feedback = Feedback.objects.all()
    filter_form = StudentFilterForm(request.GET or None)
    
    if filter_form.is_valid():
        class_name = filter_form.cleaned_data['class_name']
        section = filter_form.cleaned_data['section']
        
        if class_name and section:
            feedback = feedback.filter(classes=class_name, section=section)
    
    context = {
        
        'filter_form': filter_form,
        'feedback':feedback,
    }
    return render(request,'Admin/feedback.html',context)

def ENROLLED_STUDENT(request):
    enrolled_student = Enrollment.objects.all()
    filter_form = ClassFilterForm(request.GET or None)

        
    if filter_form.is_valid():
        class_filter = filter_form.cleaned_data.get('class_filter')
        if class_filter:
            enrolled_student = enrolled_student.filter(student_class=class_filter)

    context = {
        
        'filter_form': filter_form,
        'enrolled_student':enrolled_student,
    }
    return render(request, "Admin/enrolled_student.html",context)
def ENQUIRY_STUDENT(request):
    enquiry_student = Enquiry.objects.all().order_by('-created_at')
    context ={
        'enquiry_student':enquiry_student,
    }
    return render(request, "Admin/enquiry_student.html",context)

def STUDENT_SEE(request):
    enroll = Enrollment.objects.count()
    registered_student = StudentRegistration.objects.count()
    enquiry = Enquiry.objects.count()
    context = {
        'enroll':enroll,
        'registered_student':registered_student,
        'enquiry':enquiry,
    }
    return render(request,'Admin/student_see.html',context)


def account_section_login(request):
    if request.method == 'POST':
        form = AccountSectionPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password == settings.ACCOUNT_SECTION_PASSWORD:
                request.session['account_section_authenticated'] = True
                return redirect('accounts_home')  # Redirect to the actual account section
            else:
                form.add_error('password', 'Incorrect password.')
    else:
        form = AccountSectionPasswordForm()

    return render(request, 'Admin/account_section_login.html', {'form': form})

def student_section_login(request):
    if request.method == 'POST':
        form = StudentSectionPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password == settings.STUDENT_SECTION_PASSWORD:
                request.session['student_section_authenticated'] = True
                return redirect('list_student')  # Redirect to the actual account section
            else:
                form.add_error('password', 'Incorrect password.')
    else:
        form = StudentSectionPasswordForm()

    return render(request, 'Admin/student_section_login.html', {'form': form})


    
@admin_required
def ADD_ROUTINE(request):
    classes = Student.class_choices
    routines = Routine.objects.all().order_by('class_name')
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        routine = Routine(class_name=class_name,
                                         subject=subject,
                                         date=date,
                                         start_time=start_time,
                                         end_time= end_time,
                                         )
        routine.save()
        messages.success(request, 'Routine Added Successfully')
        return redirect('add_routine')
    return render(request, 'Admin/add_routine.html',{'classes':classes,
                                   'routines':routines})

@admin_required
def EDIT_ROUTINE(request, id):
    class_choices = Student.class_choices
    routine = Routine.objects.get(id=id)

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        routine.class_name = class_name
        routine.subject = subject
        routine.date = date 
        routine.start_time = start_time
        routine.end_time = end_time
        routine.save()

        messages.success(request, 'Routine Updated Successfully')
        return redirect('add_routine')

    # Format date and time for the template
    formatted_date = routine.date.strftime('%Y-%m-%d') if routine.date else ''
    formatted_start_time = routine.start_time.strftime('%H:%M') if routine.start_time else ''
    formatted_end_time = routine.end_time.strftime('%H:%M') if routine.end_time else ''

    context = {
        'routine': routine,
        'classes': class_choices,
        'formatted_date': formatted_date,
        'formatted_start_time': formatted_start_time,
        'formatted_end_time': formatted_end_time,
    }

    return render(request, 'Admin/edit_routine.html', context)
    
@admin_required
def DELETE_ROUTINE(request,id):
    routine = get_object_or_404(Routine,id=id)
    routine.delete()
    messages.success(request, 'Routine Deleted Successfully')
    return redirect('add_routine')

@admin_required
def DELETE_TEACHER(request,id):
    try:
        teacher = get_object_or_404(Teacher,id=id)
        user = teacher.admin  

        
        teacher.delete()
        user.delete()
        
        messages.success(request, 'Teacher Deleted Successfully')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        
    return redirect('list_teacher')

def EDIT_SESSION(request,id):
    session = get_object_or_404(Session,id=id)
    if request.method == 'POST':
        session_name=request.POST.get('session_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        session.session_name = session_name
        session.start_date = start_date
        session.end_date = end_date
        session.save()
        messages.success(request, 'Session Updated Successfully')
        return redirect('generate_admit')

def other_section_login(request):
    if request.method == 'POST':
        form = OtherSectionPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password == settings.OTHER_SECTION_PASSWORD:
                request.session['other_section_authenticated'] = True
                # Redirect to the stored 'next' URL or a default
                next_url = request.session.get('next', reverse('list_student'))
                # Clear the stored 'next' URL
                request.session.pop('next', None)
                return redirect(next_url)
            else:
                form.add_error('password', 'Incorrect password.')
    else:
        form = OtherSectionPasswordForm()

    return render(request, 'Admin/other_section_login.html', {'form': form})


from django.db.models import Sum, Q
@admin_required
@account_section_required
def DUE_BILL(request):
    if request.method == 'POST':
        form = BillFilterForm(request.POST)
        if form.is_valid():
            class_filter = form.cleaned_data.get('class_filter')
            section_filter = form.cleaned_data.get('section_filter')
            dues_filter = form.cleaned_data.get('dues_filter')
            fee_type = form.cleaned_data.get('fee_type')
            bus_name = form.cleaned_data.get('bus_name')
            
            url = reverse('generate_due_bill')
            params = {}
            if class_filter:
                params['class_filter'] = class_filter
            if section_filter:
                params['section_filter'] = section_filter
            if dues_filter:
                params['dues_filter'] = dues_filter
            if fee_type:
                params['fee_type'] = fee_type
            if bus_name:
                params['bus_name'] = bus_name
            
            return redirect(f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}")
    else:
        form = BillFilterForm()

    return render(request, 'Admin/due_bill.html', {'form': form})


@admin_required
@account_section_required
def GENERATE_DUE_BILL(request):
    class_filter = request.GET.get('class_filter')
    section_filter = request.GET.get('section_filter')
    dues_filter = request.GET.get('dues_filter')
    fee_type = request.GET.get('fee_type')
    bus_name = request.GET.get('bus_name')

    fees_with_due = Fee.objects.all()

    if class_filter:
        fees_with_due = fees_with_due.filter(student__classes=class_filter)
    
    if section_filter:
        fees_with_due = fees_with_due.filter(student__section=section_filter)

    if bus_name:
        fees_with_due = fees_with_due.filter(bus_name=bus_name)

    if dues_filter == 'with_dues':
        fees_with_due = fees_with_due.filter(
            Q(jan_status='Due') | Q(feb_status='Due') | Q(mar_status='Due') |
            Q(apr_status='Due') | Q(may_status='Due') | Q(jun_status='Due') |
            Q(jul_status='Due') | Q(aug_status='Due') | Q(sep_status='Due') |
            Q(oct_status='Due') | Q(nov_status='Due') | Q(dec_status='Due')
        )
    elif dues_filter == 'no_dues':
        fees_with_due = fees_with_due.exclude(
            Q(jan_status='Due') | Q(feb_status='Due') | Q(mar_status='Due') |
            Q(apr_status='Due') | Q(may_status='Due') | Q(jun_status='Due') |
            Q(jul_status='Due') | Q(aug_status='Due') | Q(sep_status='Due') |
            Q(oct_status='Due') | Q(nov_status='Due') | Q(dec_status='Due')
        )

    fees_with_due = fees_with_due.select_related('student')

    students_data = []
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    for fee in fees_with_due:
        due_months = []
        total_due = Decimal('0.00')

        for month in months:
            tuition_due = getattr(fee, f'{month}_due') or Decimal('0.00')
            transport_due = getattr(fee, f'{month}_transport_due') or Decimal('0.00')
            hostel_due = getattr(fee, f'{month}_hostel_due') or Decimal('0.00')

            if fee_type == 'tuition':
                relevant_due = tuition_due
            elif fee_type == 'transport':
                relevant_due = transport_due
            elif fee_type == 'hostel':
                relevant_due = hostel_due
            else:  # 'All Fees' or any other case
                relevant_due = tuition_due + transport_due + hostel_due

            if relevant_due > 0:
                due_months.append({
                    'month': month.capitalize(),
                    'tuition_due': tuition_due,
                    'transport_due': transport_due,
                    'hostel_due': hostel_due,
                    'status': getattr(fee, f'{month}_status'),
                    'payment_date': getattr(fee, f'{month}_payment_date'),
                })
                total_due += relevant_due

        if due_months or dues_filter != 'with_dues':
            total_amount_in_words = num2words(
                total_due, 
                to='currency', 
                lang='en'
            ).replace('euro', 'rupees').replace('cents', 'paise').upper()

            students_data.append({
                'student': fee.student,
                'total_due': total_due,
                'due_months': due_months,
                'fee_structure': fee.fee_structure,
                'hostel_fee': fee.hostelfee,
                'bus_name': fee.bus_name,
                'transport_fees': fee.transport_fees,
                'total_amount_in_words': total_amount_in_words
            })

    context = {
        'students_data': students_data,
        'generation_date': datetime.now().date(),
        'class_filter': class_filter or "All Classes",
        'section_filter': section_filter or "All Sections",
        'dues_filter': dict(BillFilterForm.base_fields['dues_filter'].choices).get(dues_filter, "All Students"),
        'fee_type': dict(BillFilterForm.base_fields['fee_type'].choices).get(fee_type, "All Fees"),
        'bus_name': dict(Fee.BUS_CHOICES).get(bus_name, "All Buses"),
    }

    return render(request, "Admin/generate_due_bill.html", context)


@admin_required
@account_section_required
def PRINT_ALL_DUE_BILLS(request):
    class_filter = request.GET.get('class_filter')
    section_filter = request.GET.get('section_filter')
    dues_filter = request.GET.get('dues_filter')
    fee_type = request.GET.get('fee_type')
    bus_name = request.GET.get('bus_name')

    fees_with_due = Fee.objects.all()

    if class_filter:
        fees_with_due = fees_with_due.filter(student__classes=class_filter)
    
    if section_filter:
        fees_with_due = fees_with_due.filter(student__section=section_filter)

    if bus_name:
        fees_with_due = fees_with_due.filter(bus_name=bus_name)

    if dues_filter == 'with_dues':
        fees_with_due = fees_with_due.filter(
            Q(jan_status='Due') | Q(feb_status='Due') | Q(mar_status='Due') |
            Q(apr_status='Due') | Q(may_status='Due') | Q(jun_status='Due') |
            Q(jul_status='Due') | Q(aug_status='Due') | Q(sep_status='Due') |
            Q(oct_status='Due') | Q(nov_status='Due') | Q(dec_status='Due')
        )
    elif dues_filter == 'no_dues':
        fees_with_due = fees_with_due.exclude(
            Q(jan_status='Due') | Q(feb_status='Due') | Q(mar_status='Due') |
            Q(apr_status='Due') | Q(may_status='Due') | Q(jun_status='Due') |
            Q(jul_status='Due') | Q(aug_status='Due') | Q(sep_status='Due') |
            Q(oct_status='Due') | Q(nov_status='Due') | Q(dec_status='Due')
        )

    fees_with_due = fees_with_due.select_related('student')

    students_data = []
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    for fee in fees_with_due:
        due_months = []
        total_due = Decimal('0.00')

        for month in months:
            tuition_due = getattr(fee, f'{month}_due') or Decimal('0.00')
            transport_due = getattr(fee, f'{month}_transport_due') or Decimal('0.00')
            hostel_due = getattr(fee, f'{month}_hostel_due') or Decimal('0.00')

            if fee_type == 'tuition':
                relevant_due = tuition_due
            elif fee_type == 'transport':
                relevant_due = transport_due
            elif fee_type == 'hostel':
                relevant_due = hostel_due
            else:  # 'All Fees' or any other case
                relevant_due = tuition_due + transport_due + hostel_due

            if relevant_due > 0:
                due_months.append({
                    'month': month.capitalize(),
                    'tuition_due': tuition_due,
                    'transport_due': transport_due,
                    'hostel_due': hostel_due,
                    'status': getattr(fee, f'{month}_status'),
                    'payment_date': getattr(fee, f'{month}_payment_date'),
                })
                total_due += relevant_due

        if due_months or dues_filter != 'with_dues':
            total_amount_in_words = num2words(
                total_due, 
                to='currency', 
                lang='en'
            ).replace('euro', 'rupees').replace('cents', 'paise').upper()

            students_data.append({
                'student': fee.student,
                'total_due': total_due,
                'due_months': due_months,
                'fee_structure': fee.fee_structure,
                'hostel_fee': fee.hostelfee,
                'bus_name': fee.bus_name,
                'transport_fees': fee.transport_fees,
                'total_amount_in_words': total_amount_in_words
            })

    context = {
        'students_data': students_data,
        'generation_date': datetime.now().date(),
        'class_filter': class_filter or "All Classes",
        'section_filter': section_filter or "All Sections",
        'dues_filter': dict(BillFilterForm.base_fields['dues_filter'].choices).get(dues_filter, "All Students"),
        'fee_type': dict(BillFilterForm.base_fields['fee_type'].choices).get(fee_type, "All Fees"),
        'bus_name': dict(Fee.BUS_CHOICES).get(bus_name, "All Buses"),
    }

    return render(request, "Admin/print_all_due_bills.html", context)

@admin_required
@account_section_required
def FILTER_DUE_BILLS(request):
    if request.method == 'POST':
        form = BillFilterForm(request.POST)
        if form.is_valid():
            class_filter = form.cleaned_data.get('class_filter')
            section_filter = form.cleaned_data.get('section_filter')
            dues_filter = form.cleaned_data.get('dues_filter')
            fee_type = form.cleaned_data.get('fee_type')
            bus_name = form.cleaned_data.get('bus_name')
            
            url = reverse('print_all_due_bill')
            params = {}
            if class_filter:
                params['class_filter'] = class_filter
            if section_filter:
                params['section_filter'] = section_filter
            if dues_filter:
                params['dues_filter'] = dues_filter
            if fee_type:
                params['fee_type'] = fee_type
            if bus_name:
                params['bus_name'] = bus_name
            
            return redirect(f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}")
    else:
        form = BillFilterForm()
    
    return render(request, 'Admin/filter_due_bills.html', {'form': form})


def DELETE_FEEDBACK(request,id):
    try:
        feedback = get_object_or_404(Feedback,id=id)
         

        
        feedback.delete()
        
        
        messages.success(request, 'Feedback Deleted Successfully')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        
    return redirect('feedback')

    

def EDIT_TRANSPORT_FEE(request,id):
    transport_fee = Transport_Fees.objects.get(id=id)
    if request.method == 'POST':
        transport_fee.root_name = request.POST.get('root_name')
        transport_fee.amount = request.POST.get('amount')
        transport_fee.save()
        messages.success(request, 'Transport Fee Updated Successfully')
        return redirect('view_transport_fee')
    return render(request,'Admin/edit_transport_fee.html',{'transport_fee':transport_fee})
        