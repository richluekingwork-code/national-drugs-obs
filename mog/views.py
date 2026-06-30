from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_roles
from django.shortcuts import get_object_or_404, redirect, render
from ldea.models import*
from .models import*
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from accounts.decorators import allowed_roles
from django.contrib import messages
from django.db import transaction

# Create your views here.
@login_required(login_url='dologin')
@allowed_roles(['mog_head'])
def mog_head_home(request):
    # Follow Up Visits
    followup_data = (
        FollowUpVisit.objects
        .values('visit_county')
        .annotate(total=Count('id'))
        .order_by('visit_county')
    )

    county_labels = [item['visit_county'] or 'Unknown' for item in followup_data]
    county_counts = [item['total'] for item in followup_data]

    # Beneficiary Handover
    handover_data = (
        BeneficiaryHandover.objects
        .values('follow_county')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    highest_county = None
    highest_total = 0
    lowest_county = None
    lowest_total = 0

    if handover_data:
        highest_county = handover_data.first()['follow_county']
        highest_total = handover_data.first()['total']

        lowest_county = handover_data.last()['follow_county']
        lowest_total = handover_data.last()['total']

    handover_labels = [item['follow_county'] or 'Unknown' for item in handover_data]
    handover_counts = [item['total'] for item in handover_data]

    # Child Adult Assessment By County
    assessment_data = (
        ChildAdultAssessments.objects
        .values('county')
        .annotate(total=Count('id'))
        .order_by('county')
    )

    assessment_labels = [item['county'] or 'Unknown' for item in assessment_data]
    assessment_counts = [item['total'] for item in assessment_data]

    assessment_data_count = ChildAdultAssessments.objects.count()
    followvisit_data_count = FollowUpVisit.objects.count()
    guardian_verification = FamilyTracingVerification.objects.count()
    beneficiary_verification = BeneficiaryVerification.objects.count()
    
    beneficiary_handover = BeneficiaryHandover.objects.count()
    tracing_action_taken = TracingActionTaken.objects.count()
    community_level = CommunityOutreachReport.objects.count()
    case_closure = CaseClosure.objects.count()
    
    context = {
        'county_labels': county_labels,
        'county_counts': county_counts,
        'handover_labels': handover_labels,
        'handover_counts': handover_counts,
        'highest_county': highest_county,
        'highest_total': highest_total,
        'lowest_county': lowest_county,
        'lowest_total': lowest_total,
        'assessment_labels': assessment_labels,
        'assessment_counts': assessment_counts,
        
        'assessment_data_count': assessment_data_count,
        'followvisit_data_count': followvisit_data_count,
        'guardian_verification': guardian_verification,
        'beneficiary_verification': beneficiary_verification,
        'beneficiary_handover': beneficiary_handover,
        'tracing_action_taken': tracing_action_taken,
        'community_level': community_level,
        'case_closure': case_closure,
    }
    return render(request, "mog_pages/head/index.html", context)

# ================== Mog Office View ================
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def moh_officers_home(request):

    # Follow Up Visits
    followup_data = (
        FollowUpVisit.objects
        .values('visit_county')
        .annotate(total=Count('id'))
        .order_by('visit_county')
    )

    county_labels = [item['visit_county'] or 'Unknown' for item in followup_data]
    county_counts = [item['total'] for item in followup_data]

    # Beneficiary Handover
    handover_data = (
        BeneficiaryHandover.objects
        .values('follow_county')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    highest_county = None
    highest_total = 0
    lowest_county = None
    lowest_total = 0

    if handover_data:
        highest_county = handover_data.first()['follow_county']
        highest_total = handover_data.first()['total']

        lowest_county = handover_data.last()['follow_county']
        lowest_total = handover_data.last()['total']

    handover_labels = [item['follow_county'] or 'Unknown' for item in handover_data]
    handover_counts = [item['total'] for item in handover_data]

    # Child Adult Assessment By County
    assessment_data = (
        ChildAdultAssessments.objects
        .values('county')
        .annotate(total=Count('id'))
        .order_by('county')
    )

    assessment_labels = [item['county'] or 'Unknown' for item in assessment_data]
    assessment_counts = [item['total'] for item in assessment_data]

    context = {
        'county_labels': county_labels,
        'county_counts': county_counts,

        'handover_labels': handover_labels,
        'handover_counts': handover_counts,

        'highest_county': highest_county,
        'highest_total': highest_total,

        'lowest_county': lowest_county,
        'lowest_total': lowest_total,

        'assessment_labels': assessment_labels,
        'assessment_counts': assessment_counts,
    }

    return render(request, "mog_pages/officers/index.html", context)

# -- --- Initial Assessment Form Page ------
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def mog_officers_creat_initial_assessment_form(request):
    if request.method == "POST":

        person_id = request.POST.get("person")
        person = get_object_or_404(Person, pk=person_id)
        
        ChildAdultAssessments.objects.create(

            # ==========================
            # ELIGIBILITY & CONSENT
            # ==========================
            case_meets_eligibility=bool(request.POST.get("case_meets_eligibility")),
            consent_assent_completed=bool(request.POST.get("consent_assent_completed")),
            child_adult_code=request.POST.get("child_adult_code"),
            registration_date=request.POST.get("registration_date") or None,
            county=request.POST.get("county"),

            # ==========================
            # PERSONAL INFORMATION
            # ==========================
            person=person,
            languages_spoken=request.POST.get("languages_spoken"),
            special_communication_needs=request.POST.get("special_communication_needs"),

            # ==========================
            # FATHER
            # ==========================
            father_name=request.POST.get("father_name"),
            father_date_of_birth=request.POST.get("father_date_of_birth") or None,
            father_nationality=request.POST.get("father_nationality"),
            father_county_origin=request.POST.get("father_county_origin"),
            father_district_origin=request.POST.get("father_district_origin"),
            father_status=request.POST.get("father_status"),
            father_address=request.POST.get("father_address"),
            father_contact=request.POST.get("father_contact"),

            # ==========================
            # MOTHER
            # ==========================
            mother_name=request.POST.get("mother_name"),
            mother_date_of_birth=request.POST.get("mother_date_of_birth") or None,
            mother_nationality=request.POST.get("mother_nationality"),
            mother_county_origin=request.POST.get("mother_county_origin"),
            mother_district_origin=request.POST.get("mother_district_origin"),
            mother_status=request.POST.get("mother_status"),
            mother_address=request.POST.get("mother_address"),
            mother_contact=request.POST.get("mother_contact"),

            # ==========================
            # CARE ARRANGEMENT
            # ==========================
            care_arrangement=request.POST.get("care_arrangement"),
            care_full_names = request.POST.get("care_full_name"),
            care_date_birth = request.POST.get("care_date_birth"),
            care_nationality = request.POST.get("care_nationality"),
            town_of_origin = request.POST.get("town_of_origin"),
            care_gender = request.POST.get("care_gender"),            
            cear_current_address = request.POST.get("cear_current_address"),
            care_contact_number = request.POST.get("care_contact_number"),
            
            # ==========================
            # PROTECTION CONCERNS
            # ==========================
            protection_concerns = request.POST.get("protection_concerns"),
            physical_disability = request.POST.get("physical_disability"),
            mental_illness = request.POST.get("physical_disability"),
            substances_abuse = request.POST.get("substances_abuse"),
            
            # ==========================
            # RISK
            # ==========================
            risk_level=request.POST.get("risk_level"),
            risk_summary=request.POST.get("risk_summary"),

            # ==========================
            # IMMEDIATE CONCERNS
            # ==========================
            immediate_concern=request.POST.get("immediate_concern"),
            immediate_reason=request.POST.get("immediate_reason"),
            immediate_action_taken=request.POST.get("immediate_action_taken"),
            
            # ==========================
            # CASE HISTORY
            # ==========================
            case_history=request.POST.get("case_history"),
            recommended_next_steps=request.POST.get("recommended_next_steps"),

            first_documented = request.POST.get("first_documented"),
            location_status = request.POST.get("location_status"),
            next_up_date = request.POST.get("next_up_date"),
            reporting_agency = request.POST.get("reporting_agency"),
            professional_name = request.POST.get("professional_name"),
            professional_cell = request.POST.get("professional_cell"),
            supervisor_name = request.POST.get("professional_cell"),
            supervisor_cell = request.POST.get("professional_cell"),
            social_workersignature = request.POST.get("social_workersignature"),
        )

        messages.success(request, "Assessment Saved Successfully")
        return redirect("Child_adult_assessment")
    
    used_person_ids = ChildAdultAssessments.objects.values_list("person_id", flat=True)
    get_person = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    context = {
        "get_persons": get_person,
    }
    return render(request, "mog_pages/officers/creat_initial_assessment_form.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_view_initial_assessment_form(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    assessments = ChildAdultAssessments.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        assessments = assessments.filter(created_at__year=year)

    # Filter by county
    if county:
        assessments = assessments.filter(county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "assessments": assessments,
    }
    return render(request, "mog_pages/officers/view_initial_assessment_form.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detaile_initial_assessment_form(request, id):
    assessments = ChildAdultAssessments.objects.get(id=id)
    
    context = {
       "assessments": assessments,
    }
    return render(request, "mog_pages/officers/detaile_initial_assessment_form.html", context)

# --- Follow up Form -----
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def mog_officers_create_follow_form(request):
    if request.method == "POST":

        print("POST DATA:", request.POST)  # 👈 DEBUG

        person_id = request.POST.get("person")
        if not person_id:
            messages.error(request, "Person is missing")
            return redirect("create_follow_form")

        person = get_object_or_404(Person, id=person_id)

        followed_with = request.POST.getlist("followed_with")
        followed_through = request.POST.getlist("followed_through")

        FollowUpVisit.objects.create(
            person=person,
            child_code=request.POST.get("child_code"),
            visit_county=request.POST.get("visit_county"),

            location_house=request.POST.get("location_house"),
            street=request.POST.get("street"),
            town=request.POST.get("town"),
            district=request.POST.get("district"),
            county=request.POST.get("county"),
            country=request.POST.get("country"),

            caregiver_name=request.POST.get("caregiver_name"),
            relationship=request.POST.get("relationship"),
            contact_number=request.POST.get("contact_number"),

            visit_date=request.POST.get("visit_date") or None,
            visit_number=request.POST.get("visit_number") or None,
            child_seen=request.POST.get("child_seen"),
            seen_alone=request.POST.get("seen_alone"),

            followup_date=request.POST.get("followup_date") or None,
            previous_followup_date=request.POST.get("previous_followup_date") or None,

            followed_with=followed_with,
            followed_through=followed_through,

            action_followed=request.POST.get("action_followed"),
            action_service=request.POST.get("action_service"),
            purpose_of_followup=request.POST.get("purpose_of_followup"),
            followup_details=request.POST.get("followup_details"),

            action_conducted=request.POST.get("action_conducted"),
            situation_change=request.POST.get("situation_change"),

            appearance=request.POST.get("appearance"),
            psychological_notes=request.POST.get("psychological_notes"),

            health_status=request.POST.get("health_status"),
            health_notes=request.POST.get("health_notes"),
            frequently_sick=request.POST.get("frequently_sick"),

            protection_issues=request.POST.get("protection_issues"),

            caseworker_name=request.POST.get("caseworker_name"),
            agency=request.POST.get("agency"),
            signature=request.POST.get("signature"),
        )
        messages.success(request, "Assessment Saved Successfully")
        return redirect("create_follow_form")
        
    used_person_ids = FollowUpVisit.objects.values_list("person_id", flat=True)
    get_person = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    context = {
        "get_persons": get_person,
    }
    return render(request, "mog_pages/officers/create_follow_form.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_view_follow_form(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    follow_up_from = FollowUpVisit.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        follow_up_from = follow_up_from.filter(created_at__year=year)

    # Filter by county
    if county:
        follow_up_from = follow_up_from.filter(county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "follow_up_from": follow_up_from,
    }
    return render(request, "mog_pages/officers/view_follow_form.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detail_follow_form(request, id):
    detail_follow_form = FollowUpVisit.objects.get(id=id)
    
    context = {
       "detail_follow_form": detail_follow_form,
    }
    return render(request, "mog_pages/officers/detail_follow_form.html", context)

# ---- Parent Guardian Verification ---
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def moh_officers_creat_parent_guardian_verification(request):
    
    if request.method == "POST":
        person_id = request.POST.get("person")
        person = get_object_or_404(Person, pk=person_id)

        # CREATE MAIN RECORD
        tracing = FamilyTracingVerification.objects.create(

            # BASIC INFORMATION
            person=person,
            child_code=request.POST.get("child_code"),
            follow_county=request.POST.get("follow_county"),
            center_type=request.POST.get("center_type"),
            center_type_other=request.POST.get("center_type_other"),
            separated_child=request.POST.get("separated_child") == "True",

            # FAMILY HISTORY
            mother_name=request.POST.get("mother_name"),
            mother_alive=request.POST.get("mother_alive"),
            father_name=request.POST.get("father_name"),
            father_alive=request.POST.get("father_alive"),
            guardian_alive=request.POST.get("guardian_alive"),
            parent_status=request.POST.get("parent_status"),

            # BEFORE SEPARATION
            house_location=request.POST.get("house_location"),
            street=request.POST.get("street"),
            town=request.POST.get("town"),
            district=request.POST.get("district"),
            county=request.POST.get("county"),
            country=request.POST.get("country"),
            address_information=request.POST.get("address_information"),
            child_life_information=request.POST.get("child_life_information"),
            child_memorable_events=request.POST.get("child_memorable_events"),

            # EVIDENCE
            child_id_evidence="child_id_evidence" in request.POST,
            birth_certificate_evidence="birth_certificate_evidence" in request.POST,
            photos_evidence="photos_evidence" in request.POST,
            other_evidence=request.POST.get("other_evidence"),
            child_identification_information=request.POST.get("child_identification_information"),

            # SEPARATION
            separation_date=request.POST.get("separation_date") or None,
            separation_address=request.POST.get("separation_address"),
            separated_from_name=request.POST.get("separated_from_name"),
            relationship_to_child=request.POST.get("relationship_to_child"),
            separation_circumstances=request.POST.get("separation_circumstances"),
            main_cause_of_separation=request.POST.get("main_cause_of_separation"),

            # TRACED PERSON
            traced_person_name=request.POST.get("traced_person_name"),
            traced_person_age=request.POST.get("traced_person_age") or None,
            traced_person_gender=request.POST.get("traced_person_gender"),
            traced_person_contact=request.POST.get("traced_person_contact"),
            traced_person_relationship=request.POST.get("traced_person_relationship"),
            traced_person_occupation=request.POST.get("traced_person_occupation"),

            # ACCEPTANCE
            wants_child=request.POST.get("wants_child"),
            able_to_take_care=request.POST.get("able_to_take_care"),
            alternative_family_available=request.POST.get("alternative_family_available"),

            agreement_take_child="agreement_take_child" in request.POST,
            signature_name=request.POST.get("signature_name"),

            # SIGNIFICANT INFO
            child_return_information=request.POST.get("child_return_information"),

            # CASEWORKER
            caseworker_observation=request.POST.get("caseworker_observation"),
            caseworker_name=request.POST.get("caseworker_name"),
            caseworker_date=request.POST.get("caseworker_date") or None,
            organization=request.POST.get("organization"),
        )

        # SAVE FAMILY MEMBERS (IMPORTANT PART)
        names = request.POST.getlist("family_member_name[]")
        relationships = request.POST.getlist("family_member_relationship[]")
        addresses = request.POST.getlist("family_member_address[]")

        for name, rel, addr in zip(names, relationships, addresses):
            if name:  # avoid empty rows
                FamilyMember.objects.create(tracing=tracing, name=name, relationship=rel, address=addr)

        messages.success(request, "Assessment Saved Successfully")
        return redirect("parent_guardian_verification")
    
    # GET AVAILABLE PERSONS
    used_person_ids = FamilyTracingVerification.objects.values_list("person_id", flat=True)
    get_person = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    context = {
        "get_persons": get_person,
    }
    return render(request, "mog_pages/officers/creat_guardian_verification.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def moh_officers_view_parent_guardian_verification(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    family_tracing = FamilyTracingVerification.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        family_tracing = family_tracing.filter(created_at__year=year)

    # Filter by county
    if county:
        family_tracing = family_tracing.filter(follow_county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "family_tracing": family_tracing,
    }
    return render(request, "mog_pages/officers/view_guardian_verification.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detail_parent_guardian_verification_form(request, id):
    family_tracing = FamilyTracingVerification.objects.get(id=id)
    
    context = {
       "family_tracing": family_tracing,
    }
    return render(request, "mog_pages/officers/detail_guardian_verification.html", context)

#  -- Beneficiary Verification ----- 
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def moh_officers_creat_beneficiary_verification(request):
    if request.method == "POST":
        person_id = request.POST.get("person")
        person = get_object_or_404(Person, pk=person_id)

        BeneficiaryVerification.objects.create(

            # CASE INFO
            child_code=request.POST.get("child_code"),
            case_id_number=request.POST.get("case_id_number"),
            follow_county=request.POST.get("follow_county"),
            date_completed=request.POST.get("date_completed") or None,

            # CHILD INFO
            person=person,

            current_address=request.POST.get("current_address"),
            caregiver_name=request.POST.get("caregiver_name"),

            before_separation_address=request.POST.get("before_separation_address"),
            street=request.POST.get("street"),
            town=request.POST.get("town"),
            district=request.POST.get("district"),
            county=request.POST.get("county"),
            country=request.POST.get("country"),
            other_address_info=request.POST.get("other_address_info"),

            # VERIFICATION
            match_case=request.POST.get("match_case"),
            discrepancies=request.POST.get("discrepancies"),

            child_knows_adult=request.POST.get("child_knows_adult"),
            child_comments=request.POST.get("child_comments"),
            recognize_photos=request.POST.get("recognize_photos"),

            # WISHES
            need_info=request.POST.get("need_info"),
            info_provided=request.POST.get("info_provided"),
            wants_reunification=request.POST.get("wants_reunification"),
            child_wishes_comments=request.POST.get("child_wishes_comments"),

            # RECOMMENDATION
            recommendation=request.POST.get("recommendation"),
            recommendation_reason=request.POST.get("recommendation_reason"),

            caseworker_name=request.POST.get("caseworker_name"),
            caseworker_date=request.POST.get("caseworker_date") or None,
            organization=request.POST.get("organization"),
        )

        messages.success(request, "Beneficiary Verification Report Saved Successfully")
        return redirect("creat_beneficiary_verification")
    
    used_person_ids = BeneficiaryVerification.objects.values_list("person_id", flat=True)
    get_person = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    context = {
        "get_persons": get_person,
    }  
    return render(request, "mog_pages/officers/creat_beneficiary_verification.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def moh_officers_view_beneficiary_verification(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    beneficiar_tracing = BeneficiaryVerification.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        beneficiar_tracing = beneficiar_tracing.filter(created_at__year=year)

    # Filter by county
    if county:
        beneficiar_tracing = beneficiar_tracing.filter(follow_county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "beneficiar_tracing": beneficiar_tracing,
    }
    return render(request, "mog_pages/officers/viwe_beneficiary_verification.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detail_beneficiary_verification_form(request, id):
    beneficiar_tracing = BeneficiaryVerification.objects.get(id=id)
    
    context = {
       "beneficiar_tracing": beneficiar_tracing,
    }
    return render(request, "mog_pages/officers/detail_beneficiary_verification.html", context)

# ---- Beneficiary Handover ---
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def moh_officers_creat_beneficiary_handover(request):
    if request.method == "POST":

        person = Person.objects.get(id=request.POST.get("person"))

        BeneficiaryHandover.objects.create(

            person=person,
            follow_county=request.POST.get("follow_county"),
            reunification_type=request.POST.get("reunification_type"),
            adult_verification=request.POST.get("adult_verification"),
            child_verification=request.POST.get("child_verification"),
            relationship_verified=request.POST.get("relationship_verified"),
            ongoing_support_needed=request.POST.get("ongoing_support_needed"),

            caseworker_name=request.POST.get("caseworker_name"),
            organization=request.POST.get("organization"),

            caregiver1_name=request.POST.get("caregiver1_name"),
            caregiver1_sex=request.POST.get("caregiver1_sex"),
            caregiver1_relationship=request.POST.get("caregiver1_relationship"),

            caregiver2_name=request.POST.get("caregiver2_name"),
            caregiver2_sex=request.POST.get("caregiver2_sex"),
            caregiver2_relationship=request.POST.get("caregiver2_relationship"),

            address=request.POST.get("address"),
            phone=request.POST.get("phone"),

            town_village=request.POST.get("town_village"),
            clan=request.POST.get("clan"),
            district=request.POST.get("district"),
            county=request.POST.get("county"),
            country=request.POST.get("country"),

            reunification_date=request.POST.get("reunification_date"),
            reunification_place=request.POST.get("reunification_place"),

            consent_person=request.POST.get("consent_person"),
            child_name=request.POST.get("child_name"),

            agreement_statement=request.POST.get("agreement_statement"),

            caseworker_signature=request.POST.get("caseworker_signature"),
            receiver_signature=request.POST.get("receiver_signature"),
            witness_signature=request.POST.get("witness_signature"),

            additional_information=request.POST.get("additional_information"),

            new_address_location=request.POST.get("new_address_location"),

            signature_date=request.POST.get("signature_date"),
            signature_place=request.POST.get("signature_place"),

            siblings_reunified=request.POST.get("siblings_reunified"),

            supervisor_name=request.POST.get("supervisor_name"),
            supervisor_position=request.POST.get("supervisor_position"),
        )

        messages.success(request, "Beneficiary handover saved successfully.")
        return redirect("creat_beneficiary_handover")

    used_person_ids = BeneficiaryHandover.objects.values_list("person_id", flat=True)
    get_person = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    context = {
        "get_persons": get_person,
    }  
    return render(request, "mog_pages/officers/creat_beneficiary_handover.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def moh_officers_view_beneficiary_handover(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    beneficiar_handover = BeneficiaryHandover.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        beneficiar_handover = beneficiar_handover.filter(created_at__year=year)

    # Filter by county
    if county:
        beneficiar_handover = beneficiar_handover.filter(follow_county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "beneficiar_handover": beneficiar_handover,
    }
    return render(request, "mog_pages/officers/view_beneficiary_handover.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detail_beneficiary_handover_form(request, id):
    beneficiar_handover = BeneficiaryHandover.objects.get(id=id)
    
    context = {
       "beneficiar_handover": beneficiar_handover,
    }
    return render(request, "mog_pages/officers/detail_ beneficiar_handover.html", context)

# ----- Tracing Action Taken Form ------
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def moh_officers_creat_tracing_action_taken(request):
    
    if request.method == "POST":
        person = Person.objects.get(id=request.POST.get("person"))

        tracing_record = TracingActionTaken.objects.create(
            person=person,
            follow_county=request.POST.get("follow_county"),
            tracing_notes=request.POST.get("tracing_notes"),
            caseworker_name=request.POST.get("caseworker_name"),
            caseworker_date=request.POST.get("caseworker_date"),
            caseworker_signature=request.POST.get("caseworker_signature"),
        )

        # Save the 6 tracing actions
        for i in range(1, 7):
            action_taken = request.POST.get(f"action_taken_{i}")

            if action_taken:
                TracingActionDetail.objects.create(
                    tracing_record=tracing_record,
                    action_taken=action_taken,
                    provider_details=request.POST.get(f"provider_details_{i}"),
                    individual_traced=request.POST.get(f"individual_traced_{i}"),
                    tracing_location=request.POST.get(f"tracing_location_{i}"),
                    tracing_outcome=request.POST.get(f"tracing_outcome_{i}"),
                    tracing_details=request.POST.get(f"tracing_details_{i}"),
                    next_steps=request.POST.get(f"next_steps_{i}"),
                    due_date=request.POST.get(f"due_date_{i}")
                )
        messages.success(request, "Tracing Action Record Saved Successfully.")
        return redirect("creat_tracing_action_taken")
    
    used_person_ids = TracingActionTaken.objects.values_list("person_id", flat=True)
    get_person = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    context = {
        "get_persons": get_person,
    } 
    return render(request, "mog_pages/officers/creat_tracing_action_taken.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def moh_officers_view_tracing_action_taken(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    tracing_action = TracingActionTaken.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        tracing_action = tracing_action.filter(created_at__year=year)

    # Filter by county
    if county:
        tracing_action = tracing_action.filter(follow_county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "tracing_action": tracing_action,
    }
    return render(request, "mog_pages/officers/view_tracing_action_taken.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detail_tracing_action_taken(request, id):
    tracing_action = TracingActionTaken.objects.get(id=id)

    context = {
        "tracing_action": tracing_action,
        "tracing_actions": tracing_action.actions.all()
    }
    return render(request, "mog_pages/officers/detail_tracing_action.html", context)

# -- --- Community Level Report Page ------
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def mog_officers_creat_community_level_report(request):
    if request.method == "POST":

        # =========================
        # PERSON (FOREIGN KEY FIX)
        # =========================
        person_id = request.POST.get("person")
        person = get_object_or_404(Person, pk=person_id)

        # =========================
        # CREATE REPORT
        # =========================
        CommunityOutreachReport.objects.create(

            # BASIC INFORMATION
            follow_county=request.POST.get("follow_county"),
            reporting_date=request.POST.get("reporting_date"),
            reporting_period=request.POST.get("reporting_period"),
            organization=request.POST.get("organization"),
            county_district_community=request.POST.get("county_district_community"),
            outreach_officer=request.POST.get("outreach_officer"),
            contact_information=request.POST.get("contact_information"),

            # OUTREACH ACTIVITY
            activity_date=request.POST.get("activity_date") or None,
            community_location=request.POST.get("community_location"),
            activity_type=request.POST.get("activity_type"),
            target_group=request.POST.get("target_group"),
            number_reached=request.POST.get("number_reached"),
            key_issues_identified=request.POST.get("key_issues_identified"),
            topics_discussed=request.POST.get("topics_discussed"),
            community_concerns=request.POST.get("community_concerns"),

            # YOUTH IDENTIFICATION
            person=person,

            risk_factors=request.POST.get("risk_factors"),
            immediate_needs=request.POST.get("immediate_needs"),

            # FOLLOW-UP
            followup_type=request.POST.get("followup_type"),
            followup_details=request.POST.get("followup_details"),
            progress_observed=request.POST.get("progress_observed"),
            challenges_identified=request.POST.get("challenges_identified"),
            action_taken=request.POST.get("action_taken"),
            next_followup_date=request.POST.get("next_followup_date") or None,

            emotional_condition=request.POST.get("emotional_condition"),
            family_support_status=request.POST.get("family_support_status"),
            school_attendance=request.POST.get("school_attendance"),
            behavioral_improvement=request.POST.get("behavioral_improvement"),
            additional_support_needed=request.POST.get("additional_support_needed"),

            # REFERRAL
            referral_date=request.POST.get("referral_date") or None,
            referred_by=request.POST.get("referred_by"),
            receiving_institution=request.POST.get("receiving_institution"),
            contact_person=request.POST.get("contact_person"),
            contact_number=request.POST.get("contact_number"),
            reason_for_referral=request.POST.get("reason_for_referral"),

            services_accessed=request.POST.get("services_accessed"),
            feedback_from_provider=request.POST.get("feedback_from_provider"),
            outcome=request.POST.get("outcome"),
            followup_needed=request.POST.get("followup_needed"),

            challenges=request.POST.get("challenges"),
            recommendation=request.POST.get("recommendation"),

            institution_name=request.POST.get("institution_name"),
            location=request.POST.get("location"),

            assessment_datetime=request.POST.get("assessment_datetime") or None,

            interviewee_name=request.POST.get("interviewee_name"),
            interviewee_position=request.POST.get("interviewee_position"),
            interviewee_contact=request.POST.get("interviewee_contact"),
        )

        messages.success(request, "Community Level Report Saved Successfully")
        return redirect("creat_community_Level_report")

    # =========================
    # GET METHOD
    # =========================

    used_person_ids = CommunityOutreachReport.objects.values_list("person_id", flat=True)

    get_persons = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    context = {
        "get_persons": get_persons,
    }

    return render(request, "mog_pages/officers/creat_community_Level.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def moh_officers_view_community_level_report(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    community_level_report = CommunityOutreachReport.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        community_level_report = community_level_report.filter(created_at__year=year)

    # Filter by county
    if county:
        community_level_report = community_level_report.filter(follow_county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "community_level_report": community_level_report,
    }
    return render(request, "mog_pages/officers/view_community_Level.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detail_community_level_report(request, id):
    community_level_report = CommunityOutreachReport.objects.get(id=id)

    context = {
        "community_level_report": community_level_report,
    }
    return render(request, "mog_pages/officers/detail_community_level_report.html", context)

# -- --- Community Level Report Page ------
@login_required(login_url='dologin')
@allowed_roles(['mog_officers'])
def mog_officers_creat_case_closure_form(request):
    used_person_ids = CaseClosure.objects.values_list("person_id", flat=True)
    get_persons = Person.objects.filter(role__iexact="victim").exclude(id__in=used_person_ids)

    if request.method == "POST":
        try:
            with transaction.atomic():

                person = Person.objects.get(id=request.POST.get("person"))

                case_closure = CaseClosure.objects.create(
                    person=person,
                    follow_county=request.POST.get("follow_county"),
                    case_id_number=request.POST.get("case_id_number"),
                    date_case_closed=request.POST.get("date_case_closed"),
                    primary_reason=request.POST.get("primary_reason"),
                    closure_reason_details=request.POST.get("closure_reason_details"),
                    case_opened_weeks=request.POST.get("case_opened_weeks") or None,
                    current_case_summary=request.POST.get("current_case_summary"),

                    caregiver_name=request.POST.get("caregiver_name"),
                    caregiver_relationship=request.POST.get("caregiver_relationship"),

                    county=request.POST.get("county"),
                    district=request.POST.get("district"),
                    community=request.POST.get("community"),
                    street=request.POST.get("street"),
                    caregiver_phone=request.POST.get("caregiver_phone"),

                    closure_process=request.POST.get("closure_process"),

                    child_agreed=request.POST.get("child_agreed") == "True",
                    child_reason=request.POST.get("child_reason"),

                    caregiver_agreed=request.POST.get("caregiver_agreed") == "True",
                    caregiver_reason=request.POST.get("caregiver_reason"),

                    followup_planned=request.POST.get("followup_planned") == "True",
                    followup_reason=request.POST.get("followup_reason"),

                    file_complete=request.POST.get("file_complete") == "True",
                    file_complete_reason=request.POST.get("file_complete_reason"),

                    storage_method=request.POST.get("storage_method"),
                    file_storage_until=request.POST.get("file_storage_until"),

                    contact_person_details=request.POST.get("contact_person_details"),

                    caseworker_name=request.POST.get("caseworker_name"),
                    caseworker_phone=request.POST.get("caseworker_phone"),
                    caseworker_signature=request.POST.get("caseworker_signature"),
                )

                # Child Approval
                CaseClosureApproval.objects.create(
                    case_closure=case_closure,
                    role="child",
                    name=request.POST.get("child_name"),
                    agency=request.POST.get("child_agency"),
                    contact_details=request.POST.get("child_contact"),
                    signature=request.POST.get("child_signature"),
                )

                # Caregiver Approval
                CaseClosureApproval.objects.create(
                    case_closure=case_closure,
                    role="caregiver",
                    name=request.POST.get("caregiver_approval_name"),
                    agency=request.POST.get("caregiver_agency"),
                    contact_details=request.POST.get("caregiver_contact"),
                    signature=request.POST.get("caregiver_signature"),
                )

                # Caseworker Approval
                CaseClosureApproval.objects.create(
                    case_closure=case_closure,
                    role="caseworker",
                    name=request.POST.get("caseworker_approval_name"),
                    agency=request.POST.get("caseworker_agency"),
                    contact_details=request.POST.get("caseworker_contact"),
                    signature=request.POST.get("caseworker_approval_signature"),
                )

                # Supervisor Approval
                CaseClosureApproval.objects.create(
                    case_closure=case_closure,
                    role="supervisor",
                    name=request.POST.get("supervisor_name"),
                    agency=request.POST.get("supervisor_agency"),
                    contact_details=request.POST.get("supervisor_contact"),
                    signature=request.POST.get("supervisor_signature"),
                )

                messages.success(request, "Case Closure saved successfully.")
                return redirect("creat_case_closure_form")

        except Exception as e:
            messages.error(request, f"Error saving case closure: {e}")
    context = {
        "get_persons": get_persons,
    }
    return render(request, "mog_pages/officers/creat_case_closure_form.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_view_case_closure_form(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    case_closure_form = CaseClosure.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        case_closure_form = case_closure_form.filter(created_at__year=year)

    # Filter by county
    if county:
        case_closure_form = case_closure_form.filter(follow_county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "case_closure_form": case_closure_form,
    }
    return render(request, "mog_pages/officers/view_case_closure_form.html", context)

@login_required(login_url='dologin')
@allowed_roles(['mog_officers', 'mog_head'])
def mog_officers_detail_case_closure_form(request, id):
    case_closure_form = CaseClosure.objects.get(id=id)
         
    context = {
      "case_closure_form": case_closure_form,
    }
    return render(request, "mog_pages/officers/detail_case_closure_form.html", context)
    