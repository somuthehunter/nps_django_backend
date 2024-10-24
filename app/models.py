from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage
from docx import Document
import os
from django.db.models import Sum

class StudentRegistration(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    contact = models.IntegerField()
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    class_for = models.CharField(max_length=20)
    date_of_entry = models.DateField()
    last_school_attended = models.CharField(max_length=200)
    last_class_attended = models.CharField(max_length=50)
    last_examination_attended = models.CharField(max_length=50)
    result = models.CharField(max_length=20)
    mothers_name = models.CharField(max_length=50)
    mothers_occupation = models.CharField(max_length=100)
    mothers_qualification = models.CharField(max_length=100)
    mothers_mobile_no = models.IntegerField()
    fathers_name = models.CharField(max_length=50)
    fathers_occupation = models.CharField(max_length=100)
    fathers_qualification = models.CharField(max_length=100)
    fathers_mobile_no = models.IntegerField()
    local_guardian = models.CharField(max_length=100)
    local_guardian_occupation = models.CharField(max_length=100)
    local_guardian_qualification = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.IntegerField()
    Handicapped = models.CharField(max_length=20)
    caste = models.CharField(max_length=50)
    caste_id = models.CharField(max_length=30)
    nationality = models.CharField(max_length=50)
    aadhar_no = models.IntegerField()
    religion = models.CharField(max_length=50)
    boarding_for = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=30)
    date_of_submission = models.DateField()

    def __str__(self):
        return self.name




# # Create your models here.
class CustomUser(AbstractUser):
    USER = (
        (1 , 'Hod'),
        (2 , 'Staff'),
        (3 , 'Student'),
        (4 , 'Accounts'),
        (5 , 'Back Staff'),
    )
    
    user_type = models.CharField(  max_length=50 ,default = 1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Student(models.Model):
    class_choices = [
        ('Pre-Nursery', 'Pre-Nursery'),
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('I','I'),
        ('II','II'),
        ('III','III'),
        ('IV','IV'),
        ('V','V'),
        ('VI','VI'),
        ('VII','VII'),
        ('VIII','VIII'),
        
        # Add more classes as needed
    ]
    section_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    gender = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True) 
    classes = models.CharField(choices=class_choices,max_length = 16)
    religion = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length= 15)
    admission_no =models.CharField(max_length=30)
    section = models.CharField(choices=section_choices,max_length=10,default="A")
    # student_image = models.ImageField(upload_to='media/profile_pic')
    father_name = models.CharField(max_length = 100)
    father_occupation = models.CharField(max_length = 100)
    father_mobile_number = models.CharField(max_length = 15)
    mother_name = models.CharField(max_length=50)
    mother_occupation = models.CharField(max_length=50)
    mother_mobile_number = models.CharField(max_length=15)
    present_address = models.CharField(max_length=250,null=True, blank=True)
    permanent_address = models.CharField(max_length=250,null=True, blank=True)
    roll_no = models.CharField(max_length=20)
    student_type = models.CharField(max_length=20)
    country = models.CharField(max_length=20,default="INDIA")
    
    def __str__(self):
        return self.admin.username
    # roll_no = models.CharField(max_length = 15)

    def __str__(self):
        return self.admin.first_name + "  "+ self.admin.last_name


class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    permanent_address=models.TextField()
    teaching_subject = models.CharField(max_length=200)
    qualification = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=14)
    date_of_joining = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.admin.username
    

class FeeStructure(models.Model):

    class_name = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.class_name} - {self.amount}"
    
class Transport_Fees(models.Model):
    
    root_name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.root_name} - {self.amount}"
       
class HostelFee(models.Model):
    class_name = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.class_name} - {self.amount}"


class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class TransportFee(models.Model):
#     BUS_CHOICES = [
#         ('N.A', 'N.A'),
#         ('BUS 1', 'BUS 1'),
#         ('BUS 2', 'BUS 2'),
#         ('BUS 3', 'BUS 3'),
#         ('BUS 4', 'BUS 4'),
#         ('BUS 5', 'BUS 5'),
#         ('BUS 6', 'BUS 6'),
#         ('BUS 7', 'BUS 7'),
#         ('BUS 8', 'BUS 8'),
#         ('BUS 9', 'BUS 9'),
#         ('BUS 10', 'BUS 10'),
#     ]
#     student = models.OneToOneField(Student, on_delete=models.CASCADE)
#     fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
#     hostelfee = models.ForeignKey(HostelFee,on_delete=models.CASCADE)
#     bus_name = models.CharField(choices=BUS_CHOICES,max_length=40,default='N.A')
#     transport_fees = models.ForeignKey(Transport_Fees,on_delete=models.CASCADE)
    

#     # amount = models.DecimalField(max_digits=10, decimal_places=2)
#     name=models.CharField(max_length=100,default="Transport Fee")
#     jan_payment_date = models.DateField(null=True, blank=True)
#     jan_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid' , null=True, blank=True)
#     feb_payment_date = models.DateField(null=True, blank=True)
#     feb_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', null=True, blank=True)
#     mar_payment_date = models.DateField(null=True, blank=True)
#     mar_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', null=True, blank=True)
#     apr_payment_date = models.DateField(null=True, blank=True)
#     apr_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid' , null=True, blank=True)
#     may_payment_date = models.DateField(null=True, blank=True)
#     may_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid' , null=True, blank=True)
#     jun_payment_date = models.DateField(null=True, blank=True)
#     jun_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid' , null=True, blank=True)
#     jul_payment_date = models.DateField(null=True, blank=True)
#     jul_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid' , null=True, blank=True)
#     aug_payment_date = models.DateField(null=True, blank=True)
#     aug_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', null=True, blank=True)
#     sep_payment_date = models.DateField(null=True, blank=True)
#     sep_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', null=True, blank=True)
#     oct_payment_date = models.DateField(null=True, blank=True)
#     oct_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', null=True, blank=True)
#     nov_payment_date = models.DateField(null=True, blank=True)
#     nov_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', null=True, blank=True)
#     dec_payment_date = models.DateField(null=True, blank=True)
#     dec_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', null=True, blank=True)

#     def __str__(self):
#         return f"{self.student} Monthly Fees"




class Fee(models.Model):
    BUS_CHOICES = [
        ('N.A', 'N.A'),
        ('BUS 1', 'BUS 1'),
        ('BUS 2', 'BUS 2'),
        ('BUS 3', 'BUS 3'),
        ('BUS 4', 'BUS 4'),
        ('BUS 5', 'BUS 5'),
        ('BUS 6', 'BUS 6'),
        ('BUS 7', 'BUS 7'),
        ('BUS 8', 'BUS 8'),
        ('BUS 9', 'BUS 9'),
        ('BUS 10', 'BUS 10'),
    ]
    
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE,default='N.A')
    hostelfee = models.ForeignKey(HostelFee,on_delete=models.CASCADE)
    bus_name = models.CharField(choices=BUS_CHOICES,max_length=40,default='N.A')
    transport_fees = models.ForeignKey(Transport_Fees,on_delete=models.CASCADE,default='N.A')
    
    jan_payment_date = models.DateField(null=True, blank=True)
    jan_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid') ,('Due' , 'Due')], default='Unpaid' , null=True, blank=True)
    jan_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    jan_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)  
    jan_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)  

    feb_payment_date = models.DateField(null=True, blank=True)
    feb_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid', null=True, blank=True)
    feb_due  = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    feb_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)  
    feb_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)  

    mar_payment_date = models.DateField(null=True, blank=True)
    mar_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid', null=True, blank=True)
    mar_due = models.DecimalField(max_digits=10, decimal_places=2 , default="0",null=True)
    mar_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    mar_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    apr_payment_date = models.DateField(null=True, blank=True)
    apr_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid' , null=True, blank=True)
    apr_due = models.DecimalField(max_digits=10, decimal_places=2 ,default="0",null=True)
    apr_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    apr_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    may_payment_date = models.DateField(null=True, blank=True)
    may_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid' , null=True, blank=True)
    may_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    may_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    may_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    jun_payment_date = models.DateField(null=True, blank=True)
    jun_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid' , null=True, blank=True)
    jun_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    jun_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    jun_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    jul_payment_date = models.DateField(null=True, blank=True)
    jul_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid' , null=True, blank=True)
    jul_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    jul_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    jul_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    aug_payment_date = models.DateField(null=True, blank=True)
    aug_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid', null=True, blank=True)
    aug_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    aug_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    aug_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    sep_payment_date = models.DateField(null=True, blank=True)
    sep_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid', null=True, blank=True)
    sep_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    sep_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    sep_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    oct_payment_date = models.DateField(null=True, blank=True)
    oct_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid', null=True, blank=True)
    oct_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    oct_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    oct_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    nov_payment_date = models.DateField(null=True, blank=True)
    nov_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid', null=True, blank=True)
    nov_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    nov_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    nov_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    dec_payment_date = models.DateField(null=True, blank=True)
    dec_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'),('Due' , 'Due')], default='Unpaid', null=True, blank=True)
    dec_due = models.DecimalField(max_digits=10, decimal_places=2,default="0",null=True)
    dec_transport_due = models.DecimalField(max_digits=10, decimal_places=2, default="0" , null=True)
    dec_hostel_due = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    # jan_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # feb_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # mar_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # apr_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # may_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # jun_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # jul_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # aug_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # sep_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # oct_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # nov_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)
    # dec_discount = models.DecimalField(max_digits=10, decimal_places=2, default="0", null=True)

    def __str__(self):
        return f"{self.student} Monthly Fees"
    

class Subject(models.Model):
    class_choices = [
        ('Pre-Nursery', 'Pre-Nursery'),
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('I','I'),
        ('II','II'),
        ('III','III'),
        ('IV','IV'),
        ('V','V'),
        ('VI','VI'),
        ('VII','VII'),
        ('VIII','VIII'),
        
        # Add more classes as needed
    ]
    class_name = models.CharField(choices=class_choices,max_length=20)
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_name} - {self.subject_name}"
    
class Notes(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher_name= models.CharField(max_length=80)
    notes = models.FileField(upload_to='notes/')
    note_name = models.CharField(max_length=80)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.subject} - {self.teacher_name} - {self.note_name}"

class HomeWorks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher_name= models.CharField(max_length=80)
    homework = models.FileField(upload_to='homework/')
    homework_name = models.CharField(max_length=80)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.subject} - {self.teacher_name} - {self.homework_name}"
        

    def read_file_content(self):
        if self.homework and default_storage.exists(self.homework.name):
            file_path = self.homework.path
            _, file_extension = os.path.splitext(file_path)
            
            if file_extension.lower() == '.docx':
                doc = Document(file_path)
                return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            else:
                with default_storage.open(self.homework.name, 'rb') as file:
                    return file.read().decode('utf-8', errors='ignore')
        return "No file content available."


class Staff_Notification(models.Model):
    staff = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.staff} - {self.message}"
 

class Student_Notification(models.Model):
    class_choices = [
        ('Pre-Nursery', 'Pre-Nursery'),
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('I','I'),
        ('II','II'),
        ('III','III'),
        ('IV','IV'),
        ('V','V'),
        ('VI','VI'),
        ('VII','VII'),
        ('VIII','VIII'),
       
        
        # Add more classes as needed
    ]
    class_name = models.CharField(choices=class_choices,max_length=20)
    sent_by = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.class_name} - {self.message}"

    
from django.db import models
from datetime import date

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    date = models.DateField(default=date.today)
    status_choices = [
        ('present', 'Present'),
        ('absent', 'Absent')
    ]
    status = models.CharField(choices=status_choices, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.admin.first_name} {self.student.admin.last_name} - {self.date} - {self.status}"


class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    FA_I =models.IntegerField(default=0,null=True)
    NB_I = models.IntegerField(default=0,null=True)
    SE_I = models.IntegerField(default=0,null=True)
    first_term_marks = models.IntegerField(default=0,null=True)
    FA_II = models.IntegerField(default=0,null=True)
    NB_II = models.IntegerField(default=0,null=True)
    SE_II = models.IntegerField(default=0,null=True)
    second_term_marks = models.IntegerField(default=0,null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.admin.first_name} - {self.subject.subject_name} - {self.first_term_marks} - {self.second_term_marks}"





class StudentsPayment(models.Model):
    name = models.CharField(max_length = 50)
    # student_class = models.CharField(max_length = 10)
    # parent_name = models.CharField(max_length = 50)
    amount = models.CharField(max_length = 100)
    razorpay_payment_id = models.CharField(max_length = 100 , blank = True)
    paid = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.name} - {self.amount}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE , null = True)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    classes = models.CharField(max_length= 10)
    section = models.CharField(max_length=10)
    subject = models.CharField(max_length=30)
    teacher_name = models.CharField(max_length=30)
    rating = models.CharField(max_length=20)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    CLASS_CHOICES = [
        ('Pre-Nursery', 'Pre-Nursery'),
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
        ('VI', 'VI'),
        ('VII', 'VII'),
        ('VIII', 'VIII'),
        # Add more classes as necessary
    ]

    student_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=30, choices=CLASS_CHOICES)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.email}"
    

class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']  

    def __str__(self):
        return self.name
    

class Bill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Notice(models.Model):
    TYPE = [
        ('Academic', 'Academic'),
        ('Hostel', 'Hostel'),
        ('Transport', 'Transport'),
    ]
    title = models.CharField(max_length=100)
    types = models.CharField(choices=TYPE,max_length=20)
    sent_by = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.types} -- {self.message} -- {self.sent_by}"
    
class Routine(models.Model):

    CLASS_CHOICES = [
        ('Pre-Nursery', 'Pre-Nursery'),
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('I','I'),
        ('II','II'),
        ('III','III'),
        ('IV','IV'),
        ('V','V'),
        ('VI','VI'),
        ('VII','VII'),
        ('VIII','VIII'),
        
        # Add more classes as needed
    ]
    class_name = models.CharField(choices=CLASS_CHOICES,max_length=50)
    date = models.DateField()
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.subject} on {self.date} at {self.start_time}"

    class Meta:
        ordering = ['date', 'start_time']  
        verbose_name = "Routine"
        verbose_name_plural = "Routines"


class Session(models.Model):
    session_name = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    


    def __str__(self):
        return self.session_name
    
class MarkSheetSession(models.Model):
    report_card1 = models.CharField(max_length=100)
    report_card2 = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)








    
