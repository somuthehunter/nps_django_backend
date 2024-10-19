# forms.py
from django import forms
from app.models import *

class ClassFilterForm(forms.Form):
    section_choices = Student.section_choices
    class_choices = [
        ('', 'Select Class'),
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
    class_filter = forms.ChoiceField(choices=class_choices, required=False, label='Filter by Class')
    # section = forms.ChoiceField(choices=section_choices, required=True, label="Section")



# class AttendanceFilterForm(forms.Form):
#     class_choices = Student.class_choices
#     section_choices = Student.section_choices
#     class_name = forms.ChoiceField(choices=class_choices, required=False, label="Class")
#     section_name = forms.ChoiceField(choices=section_choices,required=False,label="Section")
#     date = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}), label="Date")


class AttendanceFilterForm(forms.Form):
    class_choices = Student.class_choices
    section_choices = Student.section_choices
    class_name = forms.ChoiceField(choices=class_choices,required=False,label="Class")
    section_name = forms.ChoiceField(choices=section_choices,required=False,label="Section")
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class StudentFilterForm(forms.Form):
    class_choices = Student.class_choices
    section_choices = Student.section_choices
    class_name = forms.ChoiceField(choices=class_choices, required=True, label="Class")
    section = forms.ChoiceField(choices=section_choices, required=True, label="Section")


class FilterForm(forms.Form):
    class_choices = Student.class_choices
    section_choices = Student.section_choices
    class_name = forms.ChoiceField(choices=class_choices,required=True)  
    section = forms.ChoiceField(choices=section_choices,required=True)  
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)
    exam_term = forms.ChoiceField(choices=[('first_term', 'First Term'), ('second_term', 'Second Term')], required=False)

class ResultFilterForm(forms.Form):
    class_choices = [
        ('', 'Select Class'),
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
    section_choices = Student.section_choices

    class_name = forms.ChoiceField(choices=class_choices,required=True)  
    section = forms.ChoiceField(choices=section_choices,required=True)  
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False)
    exam_term = forms.ChoiceField(choices=[('first_term', 'First Term'), ('second_term', 'Second Term')], required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'class_name' in self.data:
            try:
                class_name = self.data.get('class_name')
                self.fields['subject'].queryset = Subject.objects.filter(class_name=class_name)
            except (ValueError, TypeError):
                pass

class ResultForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    subject_id = forms.IntegerField(widget=forms.HiddenInput())
    FA_I = forms.IntegerField(label="FA -I Marks" )
    NB_I = forms.IntegerField(label="N.B -I Marks")
    SE_I = forms.IntegerField(label="SUB ENRICH -I")
    first_term_marks = forms.IntegerField(label="First Term Marks", min_value=0, max_value=100)
    FA_II = forms.IntegerField(label="FA -I Marks" )
    NB_II = forms.IntegerField(label="N.B -I Marks")
    SE_II = forms.IntegerField(label="SUB ENRICH -I")
    second_term_marks = forms.IntegerField(label="Second Term Marks", min_value=0, max_value=100)
    
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout , Submit

class studetPayment(forms.ModelForm):
    class Meta:
        model = StudentsPayment
        fields = "__all__"
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'amount',
            Submit('submit','Submit',css_class='button white btn-block btn-primary')

        )

class AccountSectionPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class OtherSectionPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class StudentSectionPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class AttendanceSectionPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class NotificationSectionPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class FeedbackSectionPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class BillFilterForm(forms.Form):
    class_choices = [
        ('', 'Select Class'),
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
        # Add more classes as needed
    ]

    class_filter = forms.ChoiceField(
        choices=class_choices, 
        required=False, 
        label='Filter by Class'
    )

    section_filter = forms.ChoiceField(
        choices=[('', 'All Sections')] + list(Student.section_choices),
        required=False,
        label='Filter by Section'
    )

    dues_filter = forms.ChoiceField(
        choices=[
            ('', 'All Students'),
            ('with_dues', 'Students with Dues'),
            ('no_dues', 'Students without Dues')
        ],
        required=False,
        label='Filter by Dues Status'
    )
    fee_type = forms.ChoiceField(choices=[
        ('All Fees', 'All Fees'),
        ('tuition', 'Tuition'),
        ('transport', 'Transport'),
        ('hostel', 'Hostel')
        ], required=False)
    bus_name = forms.ChoiceField(choices=[('', 'All Buses')] + Fee.BUS_CHOICES, required=False)


# forms.py
from django import forms
from app import models
class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'price', 'stock', 'image']  # Add other fields as necessary
