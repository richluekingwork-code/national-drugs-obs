# signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivityLog
from .utils import get_client_ip, get_device_info


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action='login',
        ip_address=get_client_ip(request),
        device=get_device_info(request),
        description="User logged in"
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action='logout',
        ip_address=get_client_ip(request),
        device=get_device_info(request),
        description="User logged out"
    )