# utils.py
import socket

def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_device_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    return user_agent  # simple version (you can parse later)