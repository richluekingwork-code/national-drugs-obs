from django.db import models
from ldea.models import*

# Create your models here.
class DemandReduction(models.Model):
    persons = models.ManyToManyField(Person)

    treatment = models.TextField(blank=True)
    treatment_facility = models.CharField(max_length=255)    
    type_of_treatment = models.CharField(max_length=255)
    
    cases = models.CharField(max_length=100)
    injection_substance = models.CharField(max_length=10)
    drug_test = models.TextField(blank=True)

    county = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)

    psychotherapeutic_intervention = models.CharField(max_length=255)
    psychotropic_interventions = models.CharField(max_length=255)
    comorbid_conditions = models.CharField(max_length=255)
    route_of_administration = models.CharField(max_length=255)
    refer_from = models.CharField(max_length=255)
    admission_status = models.CharField(max_length=100)
    refer_to = models.CharField(max_length=255)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demand Reduction #{self.id}"

class Prevention(models.Model):

    # ---------------- INSTITUTION PROFILE ----------------
    institution_name = models.CharField(max_length=255)
    address = models.TextField()
    date = models.DateField()

    district = models.CharField(max_length=100)
    county = models.CharField(max_length=100)

    # ---------------- ACTIVITIES ----------------

    # 1. SUD Awareness + Community Names
    sud_awareness = models.BooleanField(default=False)
    sud_communities = models.TextField(blank=True, help_text="Enter community names separated by comma")

    # 2. School Health Club + School Names
    school_health_club = models.BooleanField(default=False)
    school_names = models.TextField(blank=True, help_text="Enter school names separated by comma")

    # 3. Media Campaign
    media_campaign = models.BooleanField(default=False)
    media_details = models.TextField(blank=True)

    # 4. Harm Reduction Strategies
    harm_reduction = models.BooleanField(default=False)
    harm_reduction_details = models.TextField(blank=True)

    # 5. Radio Talk Show
    radio_talk_show = models.BooleanField(default=False)
    radio_details = models.TextField(blank=True)

    # ---------------- META ----------------
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.institution_name} - {self.county}"

class TreatmentFacility(models.Model):
    FACILITY_TYPES = (
        ('inpatient', 'Inpatient Rehabilitation Center'),
        ('outpatient', 'Outpatient Treatment Center'),
        ('detox', 'Detoxification Center'),
        ('community', 'Community-Based Treatment Center'),
        ('hospital', 'Hospital-Based Treatment Unit'),
        ('private', 'Private Treatment Facility'),
        ('government', 'Government Treatment Facility'),
    )

    OWNERSHIP_TYPES = (
        ('government', 'Government'),
        ('private', 'Private'),
        ('ngo', 'NGO'),
        ('faith_based', 'Faith-Based Organization'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    )

    # FACILITY PROFILE
    facility_name = models.CharField(max_length=255)
    facility_code = models.CharField(max_length=50, unique=True)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    ownership_type = models.CharField(max_length=50, choices=OWNERSHIP_TYPES)

    # LOCATION
    county = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city_town = models.CharField(max_length=100)
    physical_address = models.TextField()

    # CONTACT INFORMATION
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    alternate_phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # LICENSING
    licensed = models.BooleanField(default=False, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    license_issue_date = models.DateField(blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)

    # CAPACITY
    total_beds = models.PositiveIntegerField(default=0)
    male_beds = models.PositiveIntegerField(default=0)
    female_beds = models.PositiveIntegerField(default=0)
    adolescent_beds = models.PositiveIntegerField(default=0)
    current_occupancy = models.PositiveIntegerField(default=0)

    # SERVICES OFFERED
    detoxification_services = models.BooleanField(default=False)
    inpatient_services = models.BooleanField(default=False)
    outpatient_services = models.BooleanField(default=False)
    counseling_services = models.BooleanField(default=False)
    family_therapy = models.BooleanField(default=False)
    group_therapy = models.BooleanField(default=False)
    medication_assisted_treatment = models.BooleanField(default=False)
    mental_health_services = models.BooleanField(default=False)
    vocational_training = models.BooleanField(default=False)
    aftercare_services = models.BooleanField(default=False)

    # STAFFING
    medical_doctors = models.PositiveIntegerField(default=0)
    psychiatrists = models.PositiveIntegerField(default=0)
    psychologists = models.PositiveIntegerField(default=0)
    nurses = models.PositiveIntegerField(default=0)
    counselors = models.PositiveIntegerField(default=0)
    social_workers = models.PositiveIntegerField(default=0)
    peer_support_workers = models.PositiveIntegerField(default=0)

    # OPERATIONS
    operational_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    accepts_referrals = models.BooleanField(default=True)
    emergency_services_available = models.BooleanField(default=False)

    # REPORTING
    reporting_year = models.PositiveIntegerField()
    reporting_quarter = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    # AUDIT
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.facility_name