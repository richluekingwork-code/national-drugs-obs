from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import*
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# Create your views here.
User = get_user_model()

ROLE_REDIRECTS = {
    # MoJ Role
    'moj_head': 'moj_head_home',
    'moj_officers': 'moj_officers_home',
    'moj_it_head': 'moj_it_head',
    # LDEA Role
    'ldea_head': 'ldea_head_home',
    'officers': 'officers_home',  
    'ldea_head_of_it': 'ldea_head_of_it_home',
    # MoH Role
    'moh_head': 'moh_head_home',
    'moh_officers': 'moh_officers_home',
    # MoG Role
    'mog_head': 'mog_head_home',
    'mog_officers': 'mog_officers_home',
    # MoY&S Role
    'moys_head': 'moys_head_home',
    'moys_officers': 'moys_officers_home',
    # Add more roles here
}

def dologin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(request, username=email, password=password)

        # Authentication failed
        if user is None:
            try:
                existing_user = User.objects.get(email=email)
                if not existing_user.is_active:
                    messages.error(request, "Your account is inactive!")
                else:
                    messages.error(request, "Incorrect password!")
            except User.DoesNotExist:
                messages.error(request, "Email not registered!")
            return redirect('dologin')

        # Inactive user
        if not user.is_active:
            messages.error(request, "Your account is inactive!")
            return redirect('dologin')

        # Login
        login(request, user)

       

        # Role-based redirect
        if user.role:
            redirect_url = ROLE_REDIRECTS.get(user.role)
            if redirect_url:
                return redirect(redirect_url)

        # No role assigned
        messages.error(request, "Your role is not assigned or not recognized!")
        return redirect('dologin')

    return render(request, "accounts_pages/logs/login.html")

def delogout(request):
    logout(request)
    return redirect('dologin') 

@login_required(login_url='dologin')
def role_based_redirect(request):

    user = request.user

    # MoJ Role URls
    if user.role == "moj_head":
        return redirect("moj_head_home")
    elif user.role == "moj_officers":
        return redirect("moj_officers_home")
    elif user.role == "moj_it_head":
        return redirect("moj_it_head")
    # LDEA Role URLs
    elif user.role == "ldea_head":
        return redirect("ldea_head_home")
    elif user.role == "officers":
        return redirect("officers_home")
    # MoH Role URLs
    elif user.role == "moh_head":
        return redirect("moh_head_home")
    elif user.role == "moh_officers":
        return redirect("moh_officers_home")
    
    # MoG Role URLs
    elif user.role == "mog_head":
        return redirect("mog_head_home") 
    
    elif user.role == "mog_officers":
        return redirect("mog_officers_home")
    
    # MoY&S Role URLs
    elif user.role == "moys_head":
        return redirect("moys_dashboard")
    # fallback
    return redirect("dologin")

@login_required(login_url='dologin')
def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    profile = None

    # ✅ Pick correct profile model
    if user.role.startswith('moj'):
        profile, created = MoJ_User.objects.get_or_create(admin=user)

    elif user.role.startswith('ldea'):
        profile, created = LDEA_User.objects.get_or_create(admin=user)

    elif user.role.startswith('moh'):
        profile, created = MoH_User.objects.get_or_create(admin=user)

    else:
        profile = None  # fallback

    if request.method == "POST":

        # ---------------- USER ----------------
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.middle_name = request.POST.get("middle_name")
        user.save()

        # ---------------- PROFILE ----------------
        if profile:
            profile.gender = request.POST.get("gender")
            profile.date_of_birth = request.POST.get("date_of_birth")
            profile.phone = request.POST.get("phone")
            profile.address = request.POST.get("address")

            profile.identification_number = request.POST.get("identification_number")
            profile.department = request.POST.get("department")

            profile.emergency_contact_name = request.POST.get("emergency_contact_name")
            profile.emergency_contact_phone = request.POST.get("emergency_contact_phone")
            profile.date_of_birth = request.POST.get("date_of_birth") or None
            
            if request.FILES.get("profile_picture"):
                profile.profile_picture = request.FILES.get("profile_picture")

            profile.save()

        messages.success(request, "Profile updated successfully ✅")
        return redirect("profile")

    context = {
        "profile": profile,
    }
    return render(request, "accounts_pages/profile/profile.html", context)

@login_required(login_url='dologin')
def my_account(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    profile = user.get_profile()

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "accounts_pages/profile/my_account.html", context)


@require_GET
def health_check(request):
    return JsonResponse({"status": "healthy", "service": "national-drug-observatory"})