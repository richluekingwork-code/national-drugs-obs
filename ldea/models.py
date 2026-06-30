from django.db import models
from django.utils.text import slugify
import uuid
from accounts.models import CustomUser, LDEA_User
from django.utils.timezone import now


class BaseModel(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    class Meta:
        abstract = True

class DrugRaid(models.Model):

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=255)

    # AUTO GENERATED (NO MORE DUPLICATES)
    reference_code = models.CharField(max_length=100, unique=True, blank=True)

    location = models.CharField(max_length=255)
    county = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)

    raid_date = models.DateField()
    raid_time = models.TimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    description = models.TextField(blank=True)

    lead_officer = models.ForeignKey(LDEA_User, on_delete=models.SET_NULL, null=True, related_name="lead_raids")

    team_members = models.ManyToManyField(LDEA_User, blank=True, related_name="team_raids")

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_raids"
    )

    total_arrests = models.PositiveIntegerField(default=0)
    total_seizures = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-raid_date']

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = f"LDEA-{now().year}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.location}"
         
class DrugType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True, help_text="E.g., Narcotic, Stimulant, Depressant")
    description = models.TextField(blank=True)
    common_units = models.CharField(max_length=50, blank=True, help_text="E.g., grams, pills, ounces")
    slug = models.SlugField(unique=True, blank=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to="seizure/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
 
class Seizure(BaseModel): 
    SEIZURE_STATUS = [
        ("stored", "Stored in Evidence Room"),
        ("destroyed", "Destroyed"),
        ("used_for_analysis", "Used for Analysis"),
        ("transferred", "Transferred to Court"),
    ]

    seizure_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    seizure_date = models.DateField()
    seizure_time = models.TimeField(null=True, blank=True)

    county = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    location_description = models.TextField(blank=True)

    seized_by = models.CharField(max_length=255)
    badge_number = models.CharField(max_length=100, blank=True)

    drug_type = models.ForeignKey(DrugType, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to="seizure/", null=True, blank=True)
    
    status = models.CharField(max_length=50, choices=SEIZURE_STATUS, default="stored")
    remarks = models.TextField(blank=True)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self.drug_type:
            self.slug = slugify(f"{self.drug_type.name}-{self.seizure_id}")
        else:
            self.slug = slugify(f"seizure-{self.seizure_id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Seizure {self.seizure_id} - {self.drug_type}"

class Person(BaseModel):

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("separated", "Separated"),                                                  
        ("widowed", "Widowed"),
        ("other", "Other"),
    ]
    
    ROLE_CHOICES = [
        ("suspect", "Suspect"),
        ("victim", "Victim"),
        ("witness", "Witness"),
    ]

    person_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    other_name = models.CharField(max_length=100, blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    professional_status = models.CharField(max_length=100, blank=True)
    educational_level = models.CharField(max_length=100, blank=True)

    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    national_id = models.CharField(max_length=50, null=True, blank=True)
    passport_number = models.CharField(max_length=50, null=True, blank=True)

    county = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(blank=True)

    occupation = models.CharField(max_length=255, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, default="Liberian")

    is_repeat_offender = models.BooleanField(default=False)
    is_under_investigation = models.BooleanField(default=False)
    drug_user = models.CharField(max_length=255, blank=True)

    photo = models.ImageField(upload_to="persons/", null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super().save(*args, **kwargs)

class Arrest(BaseModel): 
    ARREST_STATUS = [
        ("detained", "Detained"),
        ("released", "Released"),
        ("transferred", "Transferred to Court"),
    ]

    arrest_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="arrests")

    arrest_date = models.DateField()
    arrest_time = models.TimeField(null=True, blank=True)

    county = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    location_description = models.TextField(blank=True)

    arresting_officer = models.CharField(max_length=255)
    badge_number = models.CharField(max_length=100, blank=True)

    drug_type = models.CharField(max_length=100, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)

    seizure = models.CharField(max_length=100, blank=True)

    charges = models.TextField(help_text="Initial charges at arrest", blank=True)
    status = models.CharField(max_length=50, choices=ARREST_STATUS, default="detained")
    remarks = models.TextField(blank=True)
 
    def __str__(self):
        return f"Arrest - {self.person} ({self.arrest_date})"       

class VictimHistory(models.Model):
       
    DEPENDENCY_LEVEL = [
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
    ]

    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("occasional", "Occasional"),
    ]

    METHOD_CHOICES = [
        ("smoking", "Smoking"),
        ("injecting", "Injecting"),
        ("oral", "Oral"),
        ("snorting", "Snorting"),
        ("inhaling", "Inhaling"),
        ("other", "Other"),
    ]
    
    # =================================
    #       BASIC IDENTIFICATION
    # =================================
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="victim")
    incident_date = models.DateField()
    incident_time = models.TimeField(blank=True, null=True)
    incident_location = models.CharField(max_length=255)

    # =========================
    #       DRUG DETAILS
    # =========================
    primary_substance = models.CharField(max_length=255, null=True, blank=True)
    secondary_substances = models.TextField(null=True, blank=True)
    type_of_drug_used = models.TextField(null=True, blank=True)
    frequency_of_use = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True)
    last_used_date = models.DateField(null=True, blank=True)
    age_first_used = models.CharField(max_length=10, null=True, blank=True)
    duration_of_addiction_years = models.PositiveIntegerField(null=True, blank=True)
    method_of_use = models.CharField(max_length=50, choices=METHOD_CHOICES, blank=True)
    dependency_level = models.CharField(max_length=20, choices=DEPENDENCY_LEVEL, blank=True)
    
    overdose_history = models.CharField(max_length=10, null=True, blank=True)
    overdose_count = models.CharField(max_length=10, null=True, blank=True)
    
    mental_health_issues = models.CharField(max_length=10, null=True, blank=True)
    rehab_history = models.CharField(max_length=10, null=True, blank=True)
    if_rehab_yes = models.CharField(max_length=10, null=True, blank=True)
    
    arrest_reference = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person.first_name} - {self.person.last_name}"

class Cases(BaseModel):
    CASE_STATUS = [
        ("pending", "Case pending at MOJ"),
        ("investigation", "Under Investigation"),
        ("closed", "Closed"),
    ]

    case_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    case_number = models.CharField(max_length=100, unique=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    filing_date = models.DateField(auto_now_add=True)
    court_name = models.CharField(max_length=255, blank=True)
    
    county = models.CharField(max_length=50, null=True, blank=True)
    
    substance = models.CharField(max_length=255, blank=True)
    action_taken = models.CharField(max_length=255, blank=True)
    charge = models.CharField(max_length=255, blank=True)
    
    status = models.CharField(max_length=50, choices=CASE_STATUS, default="Case pending at MOJ")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.case_number}-{self.case_id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Case {self.case_number} - {self.title}"

class CaseParticipant(models.Model):
    case = models.ForeignKey(Cases, on_delete=models.CASCADE, related_name="participants")
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True) 
    is_primary = models.BooleanField(default=False, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} - {self.role}"
    
class Evidence(BaseModel):
    EVIDENCE_TYPE_CHOICES = [
        ("drug", "Drug / Narcotic"),
        ("weapon", "Weapon"),
        ("document", "Document"),
        ("electronics", "Electronics"),
        ("other", "Other"),
    ]

    EVIDENCE_STATUS = [
        ("stored", "Stored"),
        ("analyzed", "Analyzed"),
        ("destroyed", "Destroyed"),
        ("submitted_to_court", "Submitted to Court"),
    ]

    evidence_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    arrest = models.ForeignKey(Arrest, on_delete=models.SET_NULL, null=True, blank=True, related_name="evidences")
    case = models.ForeignKey(Cases, on_delete=models.SET_NULL, null=True, blank=True, related_name="evidences")
    drug_type = models.ForeignKey(DrugType, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=255)
    evidence_type = models.CharField(max_length=50, choices=EVIDENCE_TYPE_CHOICES, default="other")
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)

    county = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    location_description = models.TextField(blank=True)
    collected_by = models.CharField(max_length=255, blank=True)
    badge_number = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=50, choices=EVIDENCE_STATUS, default="stored")
    remarks = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}-{self.evidence_id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.evidence_type})"