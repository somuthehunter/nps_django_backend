from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '1':
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap

def staff_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap


def student_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '3':
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap


def account_section_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('account_section_authenticated'):
            return redirect('account_section_login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper_func



from django.shortcuts import redirect
from django.urls import reverse

def other_section_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('other_section_authenticated'):
            # Store the current path in the session
            request.session['next'] = request.get_full_path()
            return redirect('other_section_login')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def student_section_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('student_section_authenticated'):
            return redirect('student_section_login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper_func

def teacher_section_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('account_section_authenticated'):
            return redirect('account_section_login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper_func

def attendance_section_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('account_section_authenticated'):
            return redirect('account_section_login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper_func

def notification_section_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('account_section_authenticated'):
            return redirect('account_section_login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper_func

def feedback_section_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('account_section_authenticated'):
            return redirect('account_section_login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper_func

