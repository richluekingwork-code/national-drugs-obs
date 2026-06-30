from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser): # ------------ CustomUser --------------

    ROLE_CHOICES = [
        # MoJ Role
        ('moj_head', 'MOJ Head'),
        ('moj_officers', 'MOJ Officers'),
        ('moj_it_head', 'MOJ IT Head'), 
                
        # LDEA Role
        ('ldea_head', 'LDEA Head'),
        ('officers', 'Officers'), 
        ('ldea_head_of_it', 'LDEA Head of IT'), 
               
        # MoH Role               
        ('moh_head', 'MOH Head'),
        ('moh_officers', 'MOH Data Officers'),        
        
        # MoG Role  
        ('mog_head', 'MOG Head'),
        ('mog_officers', 'MOG Officers'),
        
        # MoY&S Role   
        ('moys_head', 'MOYS Head'),
        ('moys_officers', 'MoYS Head')
    ]
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='moj_it_head')
    
    def get_profile(self):
        if hasattr(self, 'MoJ_profile'):
            return self.MoJ_profile
        elif hasattr(self, 'LDEA_profile'):
            return self.LDEA_profile
        elif hasattr(self, 'MoH_profile'):
            return self.MoH_profile
        elif hasattr(self, 'MoG_profile'):
            return self.MoG_profile
        elif hasattr(self, 'MoYS_profile'):
            return self.MoYS_profile
        return None
    
    def get_profile_picture(self):
        profile = self.get_profile()
        if profile and profile.profile_picture:
            return profile.profile_picture.url
        return None
    
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

    def __str__(self):
        return self.get_full_name()

class BaseModel(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_added")
    modified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_modified")

    class Meta:
        abstract = True  

class MoJ_User(BaseModel):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="MoJ_profile")
    
    # ---------------- Personal Info ----------------
    gender = models.CharField(max_length=20, choices=[('male','Male'), ('female','Female'), ('other','Other')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)  # Useful in field operations
    identification_number = models.CharField(max_length=50, blank=True, null=True)

    # ---------------- Professional Info ----------------
    rank = models.CharField(max_length=100, blank=True)  # Officer rank, Analyst level
    department = models.CharField(max_length=100, blank=True , null=True)  # Example: Narcotics, Intelligence
    unit = models.CharField(max_length=100, blank=True)  # Sub-unit for field officers
    badge_number = models.CharField(max_length=50, blank=True)
    date_joined_agency = models.DateField(null=True, blank=True)
    service_number = models.CharField(max_length=50, blank=True)  # Optional internal service code
    
    # ---------------- Digital / Legal Info ---------------- 
    security_clearance_level = models.CharField(max_length=20, choices=[
        ('confidential','Confidential'),
        ('secret','Secret'),
        ('top_secret','Top Secret'),
    ], default='confidential')
    
    def __str__(self):
        return f"{self.admin.get_full_name()} ({self.admin.role})"
       
class LDEA_User(BaseModel):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="LDEA_profile")
    
    # ---------------- Personal Info ----------------
    gender = models.CharField(max_length=20, choices=[('male','Male'), ('female','Female'), ('other','Other')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)  # Useful in field operations
    identification_number = models.CharField(max_length=50, blank=True, null=True)  # Employee ID or Badge Number

    # ---------------- Professional Info ----------------
    rank = models.CharField(max_length=100, blank=True)  # Officer rank, Analyst level
    department = models.CharField(max_length=100, blank=True, null=True)  # Example: Narcotics, Intelligence
    unit = models.CharField(max_length=100, blank=True)  # Sub-unit for field officers
    badge_number = models.CharField(max_length=50, blank=True)
    date_joined_agency = models.DateField(null=True, blank=True)
    service_number = models.CharField(max_length=50, blank=True)  # Optional internal service code
    
    # ---------------- Digital / Legal Info ---------------- 
    security_clearance_level = models.CharField(max_length=20, choices=[
        ('confidential','Confidential'),
        ('secret','Secret'),
        ('top_secret','Top Secret'),
    ], default='confidential')
    

    def __str__(self):
        return f"{self.admin.get_full_name()} ({self.admin.role})"

class MoH_User(BaseModel):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="MoH_profile")
    
    # ---------------- Personal Info ----------------
    gender = models.CharField(max_length=20, choices=[('male','Male'), ('female','Female'), ('other','Other')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)  # Useful in field operations
    identification_number = models.CharField(max_length=50, blank=True)  # Employee ID or Badge Number

    # ---------------- Professional Info ----------------
    rank = models.CharField(max_length=100, blank=True)  # Officer rank, Analyst level
    department = models.CharField(max_length=100, blank=True)  # Example: Narcotics, Intelligence
    unit = models.CharField(max_length=100, blank=True, null=True)  # Sub-unit for field officers
    badge_number = models.CharField(max_length=50, blank=True)
    date_joined_agency = models.DateField(null=True, blank=True)
    service_number = models.CharField(max_length=50, blank=True)  # Optional internal service code
    
    # ---------------- Digital / Legal Info ---------------- 
    security_clearance_level = models.CharField(max_length=20, choices=[
        ('confidential','Confidential'),
        ('secret','Secret'),
        ('top_secret','Top Secret'),
    ], default='confidential')
    
    def __str__(self):
        return f"{self.admin.get_full_name()} ({self.admin.role})"   

class MoG_User(BaseModel):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="MoG_profile")
    
    # ---------------- Personal Info ----------------
    gender = models.CharField(max_length=20, choices=[('male','Male'), ('female','Female'), ('other','Other')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)  # Useful in field operations
    identification_number = models.CharField(max_length=50, blank=True, null=True)

    # ---------------- Professional Info ----------------
    rank = models.CharField(max_length=100, blank=True)  # Officer rank, Analyst level
    department = models.CharField(max_length=100, blank=True , null=True)  # Example: Narcotics, Intelligence
    unit = models.CharField(max_length=100, blank=True)  # Sub-unit for field officers
    badge_number = models.CharField(max_length=50, blank=True)
    date_joined_agency = models.DateField(null=True, blank=True)
    service_number = models.CharField(max_length=50, blank=True)  # Optional internal service code
    
    # ---------------- Digital / Legal Info ---------------- 
    security_clearance_level = models.CharField(max_length=20, choices=[
        ('confidential','Confidential'),
        ('secret','Secret'),
        ('top_secret','Top Secret'),
    ], default='confidential')
    
    def __str__(self):
        return f"{self.admin.get_full_name()} ({self.admin.role})"
       
class MoYS_User(BaseModel):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="MoYS_profile")
    
    # ---------------- Personal Info ----------------
    gender = models.CharField(max_length=20, choices=[('male','Male'), ('female','Female'), ('other','Other')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)  # Useful in field operations
    identification_number = models.CharField(max_length=50, blank=True)  # Employee ID or Badge Number

    # ---------------- Professional Info ----------------
    rank = models.CharField(max_length=100, blank=True)  # Officer rank, Analyst level
    department = models.CharField(max_length=100, blank=True)  # Example: Narcotics, Intelligence
    unit = models.CharField(max_length=100, blank=True)  # Sub-unit for field officers
    badge_number = models.CharField(max_length=50, blank=True)
    date_joined_agency = models.DateField(null=True, blank=True)
    service_number = models.CharField(max_length=50, blank=True)  # Optional internal service code
    
    # ---------------- Digital / Legal Info ---------------- 
    security_clearance_level = models.CharField(max_length=20, choices=[
        ('confidential','Confidential'),
        ('secret','Secret'),
        ('top_secret','Top Secret'),
    ], default='confidential')
    

    def __str__(self):
        return f"{self.admin.get_full_name()} ({self.admin.role})"

# models.py
class UserActivityLog(models.Model):

    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('update', 'Update'),
        ('create', 'Create'),
        ('delete', 'Delete'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)

    # 🌍 Tracking Info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device = models.CharField(max_length=255, blank=True)
    browser = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.created_at}"