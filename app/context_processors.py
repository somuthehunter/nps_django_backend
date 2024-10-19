# In a new file, e.g., context_processors.py
from app.models import Student_Notification

def user_notifications(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        notifications = Student_Notification.objects.filter(class_name=request.user.student.classes).order_by('-sent_at')[:5]  # Get the 5 most recent notifications
        return {'user_notifications': notifications}
    return {'user_notifications': []} 


