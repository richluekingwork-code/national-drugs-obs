from django.db import models
from ldea.models import*

# Create your models here.
class ChildAdultAssessments(models.Model):

    # 1. ELIGIBILITY & CONSENT
    case_meets_eligibility = models.BooleanField(default=False)
    consent_assent_completed = models.BooleanField(default=False)

    child_adult_code = models.CharField(max_length=100, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)

    # 2. PERSONAL INFORMATION
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    languages_spoken = models.TextField(blank=True, null=True)
    special_communication_needs = models.TextField(blank=True, null=True)

    # 4. FATHER INFORMATION
    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_date_of_birth = models.DateField(blank=True, null=True)
    father_nationality = models.CharField(max_length=255, blank=True, null=True)

    father_county_origin = models.CharField(max_length=255, blank=True, null=True)
    father_district_origin = models.CharField(max_length=255, blank=True, null=True)

    STATUS_CHOICES = (
        ('Living', 'Living'),
        ('Deceased', 'Deceased'),
        ('Missing', 'Missing'),
        ('Unknown', 'Unknown'),
    )

    father_status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    father_address = models.TextField(blank=True, null=True)
    father_contact = models.CharField(max_length=50, blank=True, null=True)

    # 5. MOTHER INFORMATION
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_date_of_birth = models.DateField(blank=True, null=True)
    mother_nationality = models.CharField(max_length=255, blank=True, null=True)
    mother_county_origin = models.CharField(max_length=255, blank=True, null=True)
    mother_district_origin = models.CharField(max_length=255, blank=True, null=True)
    mother_status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    mother_address = models.TextField(blank=True, null=True)
    mother_contact = models.CharField(max_length=50, blank=True, null=True)
        
    # 6. CURRENT CARE ARRANGEMENT
    care_arrangement = models.CharField(max_length=255, blank=True, null=True)
    care_full_names = models.CharField(max_length=255, blank=True, null=True)
    care_date_birth = models.DateField()
    care_nationality = models.CharField(max_length=255, blank=True, null=True)
    town_of_origin = models.CharField(max_length=255, blank=True, null=True)
    care_gender = models.CharField(max_length=255, blank=True, null=True)
    cear_current_address = models.CharField(max_length=255, blank=True, null=True)    
    care_contact_number = models.CharField(max_length=255, blank=True, null=True)
    
    # 7. PROTECTION CONCERNS
    protection_concerns = models.CharField(max_length=255, blank=True, null=True)
    physical_disability = models.CharField(max_length=255, blank=True, null=True)
    mental_illness = models.CharField(max_length=255, blank=True, null=True)
    substances_abuse = models.CharField(max_length=255, blank=True, null=True)
    # 8. CURRENT CAREGIVER 
    
    # 10. RISK LEVEL
    risk_level = models.CharField(max_length=255, blank=True, null=True)
    risk_summary = models.TextField(blank=True, null=True)

    # 11. IMMEDIATE CONCERNS
    immediate_concern = models.CharField(max_length=255, blank=True, null=True)
    immediate_reason = models.TextField(blank=True, null=True)
    immediate_action_taken = models.TextField(blank=True, null=True)
    
    # 12. CASE HISTORY
    case_history = models.TextField(blank=True, null=True)
    recommended_next_steps = models.TextField(blank=True, null=True)
    first_documented = models.TextField(blank=True, null=True)
    location_status = models.TextField(blank=True, null=True)
    
    next_up_date = models.DateTimeField()
    reporting_agency = models.CharField(max_length=255, blank=True, null=True)
    professional_name = models.CharField(max_length=255, blank=True, null=True)
    professional_cell = models.CharField(max_length=255, blank=True, null=True)
    supervisor_name = models.CharField(max_length=255, blank=True, null=True)
    supervisor_cell = models.CharField(max_length=255, blank=True, null=True)
    social_workersignature = models.CharField(max_length=255, blank=True, null=True)
    
    # SYSTEM FIELDS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person}"    

class FollowUpVisit(models.Model): 

    # LINK TO PERSON
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    child_code = models.CharField(max_length=100, blank=True, null=True)
    visit_county = models.CharField(max_length=100, blank=True, null=True)

    # 2. Current Living Location
    location_house = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    caregiver_name = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)

    # 3. Follow-up Visit Information
    visit_date = models.DateField(blank=True, null=True)
    visit_number = models.IntegerField(blank=True, null=True)

    child_seen = models.CharField(max_length=10, blank=True, null=True)
    seen_alone = models.CharField(max_length=10, blank=True, null=True)

    # 4. Follow-up Details
    followup_date = models.DateField(blank=True, null=True)
    previous_followup_date = models.DateField(blank=True, null=True)

    followed_with = models.JSONField(default=list, blank=True, null=True)
    followed_through = models.JSONField(default=list, blank=True, null=True)

    action_followed = models.CharField(max_length=10, blank=True, null=True)

    action_service = models.TextField(blank=True, null=True)
    purpose_of_followup = models.TextField(blank=True, null=True)
    followup_details = models.TextField(blank=True, null=True)

    action_conducted = models.CharField(max_length=20, blank=True, null=True)
    situation_change = models.CharField(max_length=20, blank=True, null=True)

    # 5. Psychological
    appearance = models.CharField(max_length=50, blank=True, null=True)
    psychological_notes = models.TextField(blank=True, null=True)

    # 6. Physical Health
    health_status = models.CharField(max_length=50, blank=True, null=True)
    health_notes = models.TextField(blank=True, null=True)
    frequently_sick = models.CharField(max_length=10, blank=True, null=True)

    # 7. Protection
    protection_issues = models.TextField(blank=True, null=True)

    # 8. Caseworker
    caseworker_name = models.CharField(max_length=255, blank=True, null=True)
    agency = models.CharField(max_length=255, blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Follow Up - {self.person}"

class FamilyTracingVerification(models.Model):

    # BASIC INFORMATION
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    child_code = models.CharField(max_length=100, blank=True, null=True)
    follow_county = models.CharField(max_length=100, blank=True, null=True)

    CENTER_CHOICES = (
        ('Orphanage', 'Orphanage'),
        ('Adoption Agency/Transit Home', 'Adoption Agency/Transit Home'),
        ('Safe Home', 'Safe Home'),
        ('Specialized Home', 'Specialized Home'),
        ('Other', 'Other'),
    )

    center_type = models.CharField(max_length=100, choices=CENTER_CHOICES, blank=True, null=True)
    center_type_other = models.CharField(max_length=255, blank=True, null=True)
    separated_child = models.BooleanField(default=False)

    # FAMILY HISTORY
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_alive = models.CharField(max_length=50, blank=True, null=True)

    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_alive = models.CharField(max_length=50, blank=True, null=True)

    guardian_alive = models.CharField(max_length=50, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)

    # INFORMATION BEFORE SEPARATION
    house_location = models.TextField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    address_information = models.TextField(blank=True, null=True)
    child_life_information = models.TextField(blank=True, null=True)
    child_memorable_events = models.TextField(blank=True, null=True)

    # EVIDENCE OF RELATIONSHIP
    child_id_evidence = models.BooleanField(default=False)
    birth_certificate_evidence = models.BooleanField(default=False)
    photos_evidence = models.BooleanField(default=False)
    other_evidence = models.CharField(max_length=255, blank=True, null=True)
    child_identification_information = models.TextField(blank=True, null=True)

    # SEPARATION DETAILS
    separation_date = models.DateField(blank=True, null=True)
    separation_address = models.TextField(blank=True, null=True)
    separated_from_name = models.CharField(max_length=255, blank=True, null=True)
    relationship_to_child = models.CharField(max_length=255, blank=True, null=True)
    separation_circumstances = models.TextField(blank=True, null=True)
    main_cause_of_separation = models.TextField(blank=True, null=True)

    # TRACED FAMILY MEMBER
    traced_person_name = models.CharField(max_length=255, blank=True, null=True)
    traced_person_age = models.PositiveIntegerField(blank=True, null=True)
    traced_person_contact = models.CharField(max_length=100, blank=True, null=True)
    traced_person_gender = models.CharField(max_length=20, blank=True, null=True)
    traced_person_relationship = models.CharField(max_length=255, blank=True, null=True)
    traced_person_occupation = models.CharField(max_length=255, blank=True, null=True)

    # ACCEPTANCE
    wants_child = models.CharField(max_length=255, blank=True, null=True)
    able_to_take_care = models.CharField(max_length=255, blank=True, null=True)
    alternative_family_available = models.CharField(max_length=255, blank=True, null=True)
    agreement_take_child = models.BooleanField(default=False)
    signature_name = models.CharField(max_length=255, blank=True, null=True)

    # SIGNIFICANT INFORMATION
    child_return_information = models.TextField(blank=True, null=True)

    # CASEWORKER OBSERVATION
    caseworker_observation = models.TextField(blank=True, null=True)
    caseworker_name = models.CharField(max_length=255, blank=True, null=True)
    caseworker_date = models.DateField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)

    # SYSTEM FIELDS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.child_code or f"Tracing #{self.id}"

class FamilyMember(models.Model):
    tracing = models.ForeignKey(FamilyTracingVerification, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"
    
class BeneficiaryVerification(models.Model):

    # CASE INFO
    child_code = models.CharField(max_length=100, blank=True, null=True)
    case_id_number = models.CharField(max_length=100, blank=True, null=True)
    follow_county = models.CharField(max_length=100, blank=True, null=True)
    date_completed = models.DateField(blank=True, null=True)

    # CHILD INFORMATION
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    current_address = models.TextField(blank=True, null=True)
    caregiver_name = models.CharField(max_length=255, blank=True, null=True)

    before_separation_address = models.TextField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    other_address_info = models.CharField(max_length=255, blank=True, null=True)

    # VERIFICATION
    match_case = models.CharField(max_length=50, blank=True, null=True)
    discrepancies = models.TextField(blank=True, null=True)

    child_knows_adult = models.CharField(max_length=50, blank=True, null=True)
    child_comments = models.TextField(blank=True, null=True)

    recognize_photos = models.CharField(max_length=50, blank=True, null=True)

    # WISHES OF CHILD
    need_info = models.CharField(max_length=50, blank=True, null=True)
    info_provided = models.CharField(max_length=50, blank=True, null=True)
    wants_reunification = models.CharField(max_length=50, blank=True, null=True)
    child_wishes_comments = models.TextField(blank=True, null=True)

    # RECOMMENDATION
    recommendation = models.CharField(max_length=255, blank=True, null=True)
    recommendation_reason = models.TextField(blank=True, null=True)

    caseworker_name = models.CharField(max_length=255, blank=True, null=True)
    caseworker_date = models.DateField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.child_code or f"Case Plan #{self.id}"  

class BeneficiaryHandover(models.Model): 
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    follow_county = models.CharField(max_length=100, blank=True, null=True)
    
    # Reunification Details
    reunification_type = models.CharField(max_length=100)
    adult_verification = models.CharField(max_length=10)
    child_verification = models.CharField(max_length=10)
    relationship_verified = models.CharField(max_length=10)
    ongoing_support_needed = models.CharField(max_length=10)

    # Handing Over
    caseworker_name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)

    caregiver1_name = models.CharField(max_length=255)
    caregiver1_sex = models.CharField(max_length=20)
    caregiver1_relationship = models.CharField(max_length=255)

    caregiver2_name = models.CharField(max_length=255)
    caregiver2_sex = models.CharField(max_length=20)
    caregiver2_relationship = models.CharField(max_length=255)

    address = models.TextField()
    phone = models.CharField(max_length=50, blank=True, null=True)

    town_village = models.CharField(max_length=255)
    clan = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    # Agreement
    reunification_date = models.DateField()
    reunification_place = models.CharField(max_length=255)

    consent_person = models.CharField(max_length=255)
    child_name = models.CharField(max_length=255)

    agreement_statement = models.TextField()

    caseworker_signature = models.CharField(max_length=255)
    receiver_signature = models.CharField(max_length=255)
    witness_signature = models.CharField(max_length=255)

    # Additional Information
    additional_information = models.TextField()

    # New Address
    new_address_location = models.TextField()

    signature_date = models.DateField()
    signature_place = models.CharField(max_length=255)

    # Siblings
    siblings_reunified = models.TextField()

    # Approval
    supervisor_name = models.CharField(max_length=255)
    supervisor_position = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person} - Beneficiary Handover"

class TracingActionTaken(models.Model):
    follow_county = models.CharField(max_length=100, blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="tracing_records")
    tracing_notes = models.TextField()
    caseworker_name = models.CharField(max_length=255)
    caseworker_date = models.DateField()
    caseworker_signature = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person} - Tracing Record"

class TracingActionDetail(models.Model):
    tracing_record = models.ForeignKey(TracingActionTaken, on_delete=models.CASCADE, related_name="actions")
    action_taken = models.CharField(max_length=255, blank=True,  null=True)
    provider_details = models.CharField(max_length=255, blank=True, null=True)
    individual_traced = models.CharField(max_length=255, blank=True, null=True)
    tracing_location = models.TextField(blank=True, null=True)
    tracing_outcome = models.CharField(max_length=100, blank=True, null=True)
    tracing_details = models.TextField(blank=True, null=True)
    next_steps = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.action_taken}"
  
class CommunityOutreachReport(models.Model):

    # =========================
    # 1. BASIC INFORMATION
    # =========================
    follow_county = models.CharField(max_length=100, blank=True, null=True)
    
    reporting_date = models.DateField()
    reporting_period = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    county_district_community = models.CharField(max_length=255)

    outreach_officer = models.CharField(max_length=255)
    contact_information = models.CharField(max_length=255)

    # =========================
    # 2. OUTREACH ACTIVITY
    # =========================
    activity_date = models.DateField(blank=True, null=True)
    community_location = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.CharField(max_length=255, blank=True, null=True)

    target_group = models.CharField(max_length=255, blank=True, null=True)
    number_reached = models.CharField(max_length=50, blank=True, null=True)
    key_issues_identified = models.TextField(blank=True, null=True)

    topics_discussed = models.TextField(blank=True, null=True)
    community_concerns = models.TextField(blank=True, null=True)

    # =========================
    # 3. YOUTH IDENTIFICATION
    # =========================
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    # Risk & Needs
    risk_factors = models.TextField(blank=True, null=True)
    immediate_needs = models.TextField(blank=True, null=True)

    # =========================
    # 4. FOLLOW-UP
    # =========================
    followup_details = models.TextField(blank=True, null=True)
    followup_type = models.CharField(max_length=255, blank=True, null=True)

    progress_observed = models.TextField(blank=True, null=True)
    challenges_identified = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)

    next_followup_date = models.DateField(blank=True, null=True)

    # Follow-up Notes
    emotional_condition = models.TextField(blank=True, null=True)
    family_support_status = models.TextField(blank=True, null=True)
    school_attendance = models.TextField(blank=True, null=True)
    behavioral_improvement = models.TextField(blank=True, null=True)
    additional_support_needed = models.TextField(blank=True, null=True)

    # =========================
    # 5. REFERRAL
    # =========================
    referral_date = models.DateField(blank=True, null=True)
    referred_by = models.CharField(max_length=255, blank=True, null=True)
    receiving_institution = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)

    reason_for_referral = models.TextField(blank=True, null=True)

    services_accessed = models.TextField(blank=True, null=True)
    feedback_from_provider = models.TextField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    followup_needed = models.TextField(blank=True, null=True)

    challenges = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)

    # Assessment details
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    assessment_datetime = models.DateTimeField(blank=True, null=True)

    interviewee_name = models.CharField(max_length=255, blank=True, null=True)
    interviewee_position = models.CharField(max_length=255, blank=True, null=True)
    interviewee_contact = models.CharField(max_length=50, blank=True, null=True)

    # =========================
    # 6. META INFO
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Community Outreach Report - {self.reporting_date}"
   
class CaseClosure(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="case_closures")
    follow_county = models.CharField(max_length=100, blank=True, null=True)
    case_id_number = models.CharField(max_length=100)
    date_case_closed = models.DateField()
    primary_reason = models.CharField(max_length=255)
    closure_reason_details = models.TextField(blank=True)
    case_opened_weeks = models.PositiveIntegerField(null=True, blank=True)
    current_case_summary = models.TextField()
    caregiver_name = models.CharField(max_length=255, blank=True)
    caregiver_relationship = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    community = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    caregiver_phone = models.CharField(max_length=100, blank=True)
    closure_process = models.TextField()
    child_agreed = models.BooleanField(default=False)
    child_reason = models.TextField(blank=True)
    caregiver_agreed = models.BooleanField(default=False)
    caregiver_reason = models.TextField(blank=True)
    followup_planned = models.BooleanField(default=False)
    followup_reason = models.TextField(blank=True)
    file_complete = models.BooleanField(default=False)
    file_complete_reason = models.TextField(blank=True)

    storage_method = models.CharField(
        max_length=50,
        choices=[
            ("electronic", "Electronic"),
            ("hardcopy", "Hard Copy"),
            ("both", "Both")
        ]
    )

    file_storage_until = models.DateField(null=True, blank=True)
    child_informed = models.BooleanField(default=False)
    child_informed_reason = models.TextField(blank=True)
    contact_person_details = models.TextField(blank=True)
    caseworker_name = models.CharField(max_length=255)
    caseworker_phone = models.CharField(max_length=100)
    caseworker_signature = models.CharField(max_length=255)
    
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} - Case Closure"
    
class CaseClosureApproval(models.Model):
    case_closure = models.ForeignKey(CaseClosure, on_delete=models.CASCADE, related_name="approvals")

    ROLE_CHOICES = [
        ("child", "Child"),
        ("caregiver", "Caregiver"),
        ("caseworker", "Caseworker"),
        ("supervisor", "Supervisor"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=255)
    agency = models.CharField(max_length=255, blank=True)
    contact_details = models.CharField(max_length=255, blank=True)
    signature = models.CharField(max_length=255, blank=True)
       
 