from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_roles
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import*
from .models import*
from django.utils.dateparse import parse_date
from datetime import date

import json
import time
from django.db.models import Count
from django.db.models import Avg, Case, When, FloatField
from django.db.models.functions import ExtractYear
from collections import defaultdict
from django.db.models import Q



# Create your views here.
#===================================
#       Moj Head Views
#===================================
@login_required(login_url='dologin')
@allowed_roles(['moj_head'])
def moj_head_home(request):
    year = request.GET.get("year")

    # YEARS FOR FILTER
    arrests = Arrest.objects.exclude(arrest_date__isnull=True)
    years = (
        arrests
        .annotate(year=ExtractYear("arrest_date"))
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )

    if year:
        try:
            year = int(year)
            arrests = arrests.filter(arrest_date__year=year)
        except ValueError:
            arrests = Arrest.objects.none()

    # EFFECTIVENESS FOR ARRESTS
    arrests = (
        arrests
        .values("arrest_date")
        .annotate(
            effectiveness_score=Case(
                When(status="transferred", then=100),
                When(status="detained", then=50),
                When(status="released", then=0),
                default=0,
                output_field=FloatField()
            )
        )
        .annotate(avg_effectiveness=Avg("effectiveness_score"))
        .order_by("arrest_date")
    )

    chart_data_arrests = [
        [int(time.mktime(item["arrest_date"].timetuple())) * 1000, round(item["avg_effectiveness"], 2)]
        for item in arrests if item["arrest_date"]
    ]

    # NEW SUBSTANCES TIME SERIES
    seizures = Seizure.objects.exclude(seizure_date__isnull=True)
    if year:
        seizures = seizures.filter(seizure_date__year=year)

    # Group by date and drug_type
    substance_series = {}
    dates = seizures.values_list('seizure_date', flat=True).distinct().order_by('seizure_date')

    for drug in seizures.values('drug_type__name').distinct():
        name = drug['drug_type__name'] or "Unknown"
        series_data = []
        for d in dates:
            count = seizures.filter(seizure_date=d, drug_type__name=name).count()
            timestamp = int(time.mktime(d.timetuple())) * 1000
            series_data.append([timestamp, count])
        substance_series[name] = series_data

    # Prepare series for JS
    series = [{"name": k, "data": v} for k, v in substance_series.items()]
    
    # MOST TRAFFICKED DRUGS
    drug_counts = (
        seizures
        .values("drug_type__name")
        .annotate(count=Count("drug_type"))
        .order_by("-count")
    )

    # Labels and counts for chart
    drug_labels = [d["drug_type__name"] or "Unknown" for d in drug_counts]
    drug_values = [d["count"] for d in drug_counts]

    # DRUG HOTSPOTS ANALYSIS
    hotspots = (
        seizures
        .values("county")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    hotspot_labels = [h["county"] or "Unknown" for h in hotspots]
    hotspot_values = [h["count"] for h in hotspots]

    county_data = (
        CourtUpdate.objects
        .filter(court_case__participants__role__iexact="suspect")
        .values('county')
        .annotate(total=Count('court_case__participants'))
        .order_by('-total')
    )

    counties = [c['county'] for c in county_data if c['county']]
    totals = [c['total'] for c in county_data if c['county']]

    victim_data = (
        VictimDetails.objects
        .values('county')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    counties = [v['county'] for v in victim_data if v['county']]
    totals = [v['total'] for v in victim_data if v['county']]
    
    cases = Cases.objects.all().count()
    evidence = Evidence.objects.all().count()
    drug_raid = DrugRaid.objects.all().count()
    new_drug = DrugType.objects.all().count()

    context = {
        "victim_counties": json.dumps(counties),
        "victim_totals": json.dumps(totals),
        
        "counties": json.dumps(counties),
        "totals": json.dumps(totals),
        
        "cases": cases,
        "evidence": evidence,
        "drug_raid": drug_raid,
        "new_drug": new_drug,
        
        "effectiveness_data": json.dumps(chart_data_arrests),
        "selected_year": year,
        "years": years,
        "substance_series": json.dumps(series), 
        "drug_labels": json.dumps(drug_labels), 
        "drug_values": json.dumps(drug_values),
        "hotspot_labels": json.dumps(hotspot_labels),
        "hotspot_values": json.dumps(hotspot_values),
    }
    return render(request, "moj_pages/head/index.html", context)


#===================================
#       MOJ Officers Views
#===================================

# ------ Home ---------
@login_required(login_url='dologin')
@allowed_roles(['moj_officers'])
def moj_officers_home(request):
    year = request.GET.get("year")

    # YEARS FOR FILTER
    arrests = Arrest.objects.exclude(arrest_date__isnull=True)
    years = (
        arrests
        .annotate(year=ExtractYear("arrest_date"))
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )

    if year:
        try:
            year = int(year)
            arrests = arrests.filter(arrest_date__year=year)
        except ValueError:
            arrests = Arrest.objects.none()

    # EFFECTIVENESS FOR ARRESTS
    arrests = (
        arrests
        .values("arrest_date")
        .annotate(
            effectiveness_score=Case(
                When(status="transferred", then=100),
                When(status="detained", then=50),
                When(status="released", then=0),
                default=0,
                output_field=FloatField()
            )
        )
        .annotate(avg_effectiveness=Avg("effectiveness_score"))
        .order_by("arrest_date")
    )

    chart_data_arrests = [
        [int(time.mktime(item["arrest_date"].timetuple())) * 1000, round(item["avg_effectiveness"], 2)]
        for item in arrests if item["arrest_date"]
    ]

    # NEW SUBSTANCES TIME SERIES
    seizures = Seizure.objects.exclude(seizure_date__isnull=True)
    if year:
        seizures = seizures.filter(seizure_date__year=year)

    # Group by date and drug_type
    substance_series = {}
    dates = seizures.values_list('seizure_date', flat=True).distinct().order_by('seizure_date')

    for drug in seizures.values('drug_type__name').distinct():
        name = drug['drug_type__name'] or "Unknown"
        series_data = []
        for d in dates:
            count = seizures.filter(seizure_date=d, drug_type__name=name).count()
            timestamp = int(time.mktime(d.timetuple())) * 1000
            series_data.append([timestamp, count])
        substance_series[name] = series_data

    # Prepare series for JS
    series = [{"name": k, "data": v} for k, v in substance_series.items()]
    
    # MOST TRAFFICKED DRUGS
    drug_counts = (
        seizures
        .values("drug_type__name")
        .annotate(count=Count("drug_type"))
        .order_by("-count")
    )

    # Labels and counts for chart
    drug_labels = [d["drug_type__name"] or "Unknown" for d in drug_counts]
    drug_values = [d["count"] for d in drug_counts]

    # DRUG HOTSPOTS ANALYSIS
    hotspots = (
        seizures
        .values("county")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    hotspot_labels = [h["county"] or "Unknown" for h in hotspots]
    hotspot_values = [h["count"] for h in hotspots]

    county_data = (
        CourtUpdate.objects
        .filter(court_case__participants__role__iexact="suspect")
        .values('county')
        .annotate(total=Count('court_case__participants'))
        .order_by('-total')
    )

    counties = [c['county'] for c in county_data if c['county']]
    totals = [c['total'] for c in county_data if c['county']]

    victim_data = (
        VictimDetails.objects
        .values('county')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    counties = [v['county'] for v in victim_data if v['county']]
    totals = [v['total'] for v in victim_data if v['county']]
    
    cases = Cases.objects.all().count()
    evidence = Evidence.objects.all().count()
    drug_raid = DrugRaid.objects.all().count()
    new_drug = DrugType.objects.all().count()

    context = {
        "victim_counties": json.dumps(counties),
        "victim_totals": json.dumps(totals),
        
        "counties": json.dumps(counties),
        "totals": json.dumps(totals),
        
        "cases": cases,
        "evidence": evidence,
        "drug_raid": drug_raid,
        "new_drug": new_drug,
        
        "effectiveness_data": json.dumps(chart_data_arrests),
        "selected_year": year,
        "years": years,
        "substance_series": json.dumps(series), 
        "drug_labels": json.dumps(drug_labels), 
        "drug_values": json.dumps(drug_values),
        "hotspot_labels": json.dumps(hotspot_labels),
        "hotspot_values": json.dumps(hotspot_values),
    }
    return render(request, "moj_pages/officers/index.html", context)

# ------ create and view court cases update ---------
@login_required(login_url='dologin')
@allowed_roles(['moj_officers'])
def moj_officers_create_court_cases_update(request):
    
    # Get all cases for dropdown
    cases = Cases.objects.filter(updates__isnull=True).distinct()

    if request.method == "POST":
        court_case_id = request.POST.get("court_case")
        update_date = request.POST.get("update_date")
        status = request.POST.get("status")
        next_hearing_date = request.POST.get("next_hearing_date")
        notes = request.POST.get("notes")
        court = request.POST.get("court")
        county = request.POST.get("county")
        court_case = get_object_or_404(Cases, id=court_case_id)

        CourtUpdate.objects.create(
            court_case=court_case,
            update_date=update_date,
            status=status,
            next_hearing_date=next_hearing_date if next_hearing_date else None,
            notes=notes,
            court=court,
            county=county,
            updated_by=request.user
        )
        messages.success(request, "Court update saved successfully")
        return redirect("create_cases_update")

    context = {
        "cases": cases
    }
    return render(request, "moj_pages/officers/create_court_cases_update.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_officers', 'moj_head'])
def moj_officers_view_court_cases_update(request):
    action = request.GET.get("action")

    year = request.GET.get("year")
    county = request.GET.get("county")

    court_updates = CourtUpdate.objects.all()

    # Clean inputs
    if year:
        year = year.strip()
    if county:
        county = county.strip()

    # ✅ Filter by year
    if year:
        try:
            court_updates = court_updates.filter(update_date__year=int(year))
        except ValueError:
            pass

    # ✅ Filter by county
    if county:
        court_updates = court_updates.filter(county__icontains=county)

    context = {
        "action": action,
        "court_updates": court_updates,
        "year": year,
        "county": county,
    }
    return render(request, "moj_pages/officers/view_court_cases_update.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_officers', 'moj_head'])
def moj_officers_court_cases_detail(request, id):
    view_court_case = get_object_or_404(CourtUpdate, id=id)
    case = view_court_case.court_case

    # ✅ filter suspects only
    participants = case.participants.filter(role="suspect")

    charges_list = case.charge.split(",") if case.charge else []

    evidence_list = []
    if case.substance:
        evidence_list = [e.strip() for e in case.substance.split(",")]

    primary_suspect = participants.filter(is_primary=True).first()

    context = {
        "view_court_case": view_court_case,
        "case": case,
        "participants": participants,  # now ONLY suspects
        "charges_list": charges_list,
        "evidence_list": evidence_list,
        "primary_suspect": primary_suspect,
    }
    return render(request, "moj_pages/officers/cases_update_details.html", context)

# ------ create and view victim details ---------
@login_required(login_url='dologin')
@allowed_roles(['moj_officers'])
def moj_officers_create_victim_details(request):
    # Only victims NOT already referred
    participants = CaseParticipant.objects.filter(
        role="victim",
        victimdetails__isnull=True  # avoids duplicates automatically
    )

    if request.method == "POST":
        participant_id = request.POST.get("participant")
        condition = request.POST.get("condition")
        referred_to_moh = request.POST.get("referred_to_moh") == "on"
        referral_date = request.POST.get("referral_date")
        treatment_status = request.POST.get("treatment_status")
        facility_name = request.POST.get("facility_name")
        notes = request.POST.get("notes")
        county = request.POST.get("county")

        # Validate participant
        participant = get_object_or_404(CaseParticipant, id=participant_id, role="victim")

        # Prevent duplicate manually (extra safety)
        if VictimDetails.objects.filter(participant=participant).exists():
            messages.warning(request, "This victim has already been referred.")
            return redirect("create_victim_details")

        # Create record
        VictimDetails.objects.create(
            participant=participant,
            condition=condition,
            referred_by=request.user,
            referred_to_moh=referred_to_moh,
            referral_date=referral_date if referral_date else date.today(),
            treatment_status=treatment_status,
            facility_name=facility_name,
            county=county,
            notes=notes
        )

        messages.success(request, "Victim successfully referred to MoH.")
        return redirect("create_victim_details")

    context = {
        "participants": participants
    }
    return render(request, "moj_pages/officers/create_victim_details.html", context)

@login_required(login_url='dologin') 
@allowed_roles(['moj_officers'])
def moj_officers_view_victim_details(request):
    action = request.GET.get("action")

    year = request.GET.get("year")
    county = request.GET.get("county")

    # Load with relationships (VERY IMPORTANT)
    victims = VictimDetails.objects.select_related(
        "participant__person"
    ).all()

    # FILTER BY YEAR (from BaseModel created_at)
    if year:
        try:
            victims = victims.filter(created_at__year=int(year))
        except ValueError:
            victims = VictimDetails.objects.none()

    # FILTER BY COUNTY (from Person model)
    if county:
        victims = victims.filter(participant__person__county=county)

    # OPTIONAL: Ensure only real victims
    victims = victims.filter(participant__role__iexact="victim")

    context = {
        "action": action,
        "victims": victims,
        "selected_year": year,
        "selected_county": county,
    }
    return render(request, "moj_pages/officers/view_victim_details.html", context)

#===================================
#       MoJ IT Head Views
#===================================
@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_admin_home(request):
    # Count users
    count_moj = MoJ_User.objects.count()
    count_ldea = LDEA_User.objects.count()
    count_moh = MoH_User.objects.count()
    
    count_mog = MoG_User.objects.count()
    count_moys = MoYS_User.objects.count()
    
    data = {
            "MoJ": MoJ_User.objects.count(),
            "LDEA": LDEA_User.objects.count(),
            "MoH": MoH_User.objects.count(),
            "MoG": MoG_User.objects.count(),
            "MoYS": MoYS_User.objects.count(),
        }

        # find highest & lowest
    highest = max(data, key=data.get)
    lowest = min(data, key=data.get)

    context = {
        "labels": list(data.keys()),
        "values": list(data.values()),
        "highest": highest,
        "lowest": lowest,
        
        "count_moj": count_moj,
        "count_ldea": count_ldea,
        "count_moh": count_moh,
        "count_mog": count_mog,
        "count_moys": count_moys,
    }
    return render(request, "moj_pages/admin/index.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_create_ldea_account(request):
    if request.method == "POST":

        # ------------------- Personal Info -------------------
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        profile_picture = request.FILES.get("profile_picture")
        emergency_contact_name = request.POST.get("emergency_contact_name")
        emergency_contact_phone = request.POST.get("emergency_contact_phone")
        blood_type = request.POST.get("blood_type")
        identification_number = request.POST.get("identification_number")

        # ------------------- Professional Info -------------------
        role = request.POST.get("role")
        rank = request.POST.get("rank")
        department = request.POST.get("department")
        unit = request.POST.get("unit")
        badge_number = request.POST.get("badge_number")
        date_joined_agency = request.POST.get("date_joined_agency")
        service_number = request.POST.get("service_number")
        security_clearance_level = request.POST.get("security_clearance_level")

        # ------------------- Account Info -------------------
        username = request.POST.get("user_name")
        password = request.POST.get("password")

        # ------------------- Validation -------------------
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("ceate_ldea_account")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("ceate_ldea_account")

        # ------------------- Create User (IMPORTANT FIX) -------------------
        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            password=password,  
            role=role,
            is_active=True,
        )

        # ------------------- Create LDEA_User Profile -------------------
        LDEA_User.objects.create(
            admin=user,
            gender=gender,
            date_of_birth=parse_date(date_of_birth) if date_of_birth else None,
            phone=phone,
            email=email,
            address=address,
            profile_picture=profile_picture,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            blood_type=blood_type,
            identification_number=identification_number,
            rank=rank,
            department=department,
            unit=unit,
            badge_number=badge_number,
            date_joined_agency=parse_date(date_joined_agency) if date_joined_agency else None,
            service_number=service_number,
            security_clearance_level=security_clearance_level,
        )

        # ------------------- Success Message -------------------
        messages.success(request, f"LDEA account for {user.get_full_name()} created successfully!")
        return redirect("ceate_ldea_account")

    context = {}
    return render(request, "moj_pages/admin/ceate_ldea_account.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_view_ldea_account(request):
    view_ldea_user = LDEA_User.objects.all().order_by('rank')
    
    context = {
        "view_ldea_user": view_ldea_user
    }
    return render(request, "moj_pages/admin/view_ldea_account.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_create_account(request):
    if request.method == "POST":

        # ------------------- Personal Info -------------------
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        profile_picture = request.FILES.get("profile_picture")
        emergency_contact_name = request.POST.get("emergency_contact_name")
        emergency_contact_phone = request.POST.get("emergency_contact_phone")
        blood_type = request.POST.get("blood_type")
        identification_number = request.POST.get("identification_number")

        # ------------------- Professional Info -------------------
        role = request.POST.get("role")
        rank = request.POST.get("rank")
        department = request.POST.get("department")
        unit = request.POST.get("unit")
        badge_number = request.POST.get("badge_number")
        date_joined_agency = request.POST.get("date_joined_agency")
        service_number = request.POST.get("service_number")
        security_clearance_level = request.POST.get("security_clearance_level")

        # ------------------- Account Info -------------------
        username = request.POST.get("user_name")
        password = request.POST.get("password")

        # ------------------- Validation -------------------
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("ceate_moj_account")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("ceate_moj_account")

        # ------------------- Create User (IMPORTANT FIX) -------------------
        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            password=password,  
            role=role,
            is_active=True,
        )
        # ------------------- Create MoJ_User Profile -------------------
        MoJ_User.objects.create(
            admin=user,
            gender=gender,
            date_of_birth=parse_date(date_of_birth) if date_of_birth else None,
            phone=phone,
            email=email,
            address=address,
            profile_picture=profile_picture,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            blood_type=blood_type,
            identification_number=identification_number,
            rank=rank,
            department=department,
            unit=unit,
            badge_number=badge_number,
            date_joined_agency=parse_date(date_joined_agency) if date_joined_agency else None,
            service_number=service_number,
            security_clearance_level=security_clearance_level,
        )

        # ------------------- Success Message -------------------
        messages.success(request, f"MoJ account for {user.get_full_name()} created successfully!")
        return redirect("ceate_moj_account")
    contex = {}
    return render(request, "moj_pages/admin/ceate_moj_account.html", contex)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_view_account(request):
    view_moj_user = MoJ_User.objects.all().order_by('rank')
    
    context = {
        "view_moj_user": view_moj_user
    }
    return render(request, "moj_pages/admin/view_moj_account.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_create_moh_account(request):
    if request.method == "POST":

        role = request.POST.get("role")

        if not role:
            messages.error(request, "Please select a role")
            return redirect("ceate_moh_account")

        email = request.POST.get("email")
        username = request.POST.get("user_name")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("ceate_moh_account")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("ceate_moh_account")

        user = CustomUser.objects.create_user(
            username=username,
            first_name=request.POST.get("first_name"),
            middle_name=request.POST.get("middle_name"),
            last_name=request.POST.get("last_name"),
            email=email,
            password=request.POST.get("password"),
            role=role,
            is_active=True,
        )

        MoH_User.objects.create(
            admin=user,
            gender=request.POST.get("gender"),
            phone=request.POST.get("phone"),
            email=email,
            address=request.POST.get("address"),
            profile_picture=request.FILES.get("profile_picture"),
            emergency_contact_name=request.POST.get("emergency_contact_name"),
            emergency_contact_phone=request.POST.get("emergency_contact_phone"),
            blood_type=request.POST.get("blood_type"),
            identification_number=request.POST.get("identification_number"),
            rank=request.POST.get("rank"),
            department=request.POST.get("department"),
            unit=request.POST.get("unit"),
            badge_number=request.POST.get("badge_number"),
            service_number=request.POST.get("service_number"),
            security_clearance_level=request.POST.get("security_clearance_level"),
        )

        messages.success(request, f"MoH account for {user.get_full_name()} created successfully!")
        return redirect("ceate_moh_account")

    contex = {}
    return render(request, "moj_pages/admin/ceate_moh_account.html", contex)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moh_view_account(request):
    view_moh_user = MoH_User.objects.all().order_by('rank')
    
    context = {
        "view_moh_user": view_moh_user
    }
    return render(request, "moj_pages/admin/view_moh_account.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_create_mog_account(request):
    if request.method == "POST":

        role = request.POST.get("role")

        if not role:
            messages.error(request, "Please select a role")
            return redirect("ceate_moh_account")

        email = request.POST.get("email")
        username = request.POST.get("user_name")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("ceate_moh_account")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("ceate_moh_account")

        user = CustomUser.objects.create_user(
            username=username,
            first_name=request.POST.get("first_name"),
            middle_name=request.POST.get("middle_name"),
            last_name=request.POST.get("last_name"),
            email=email,
            password=request.POST.get("password"),
            role=role,
            is_active=True,
        )

        MoG_User.objects.create(
            admin=user,
            gender=request.POST.get("gender"),
            phone=request.POST.get("phone"),
            email=email,
            address=request.POST.get("address"),
            profile_picture=request.FILES.get("profile_picture"),
            emergency_contact_name=request.POST.get("emergency_contact_name"),
            emergency_contact_phone=request.POST.get("emergency_contact_phone"),
            blood_type=request.POST.get("blood_type"),
            identification_number=request.POST.get("identification_number"),
            rank=request.POST.get("rank"),
            department=request.POST.get("department"),
            unit=request.POST.get("unit"),
            badge_number=request.POST.get("badge_number"),
            service_number=request.POST.get("service_number"),
            security_clearance_level=request.POST.get("security_clearance_level"),
        )

        messages.success(request, f"MoG account for {user.get_full_name()} created successfully!")
        return redirect("ceate_mog_account")

    contex = {}
    return render(request, "moj_pages/admin/ceate_mog_account.html", contex)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_view_mog_account(request):
    view_mog_user = MoG_User.objects.all().order_by('rank')
    
    context = {
        "view_mog_user": view_mog_user
    }
    return render(request, "moj_pages/admin/view_mog_account.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_create_moys_account(request):
    if request.method == "POST":

        role = request.POST.get("role")

        if not role:
            messages.error(request, "Please select a role")
            return redirect("ceate_moh_account")

        email = request.POST.get("email")
        username = request.POST.get("user_name")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("ceate_moh_account")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("ceate_moh_account")

        user = CustomUser.objects.create_user(
            username=username,
            first_name=request.POST.get("first_name"),
            middle_name=request.POST.get("middle_name"),
            last_name=request.POST.get("last_name"),
            email=email,
            password=request.POST.get("password"),
            role=role,
            is_active=True,
        )

        MoYS_User.objects.create(
            admin=user,
            gender=request.POST.get("gender"),
            phone=request.POST.get("phone"),
            email=email,
            address=request.POST.get("address"),
            profile_picture=request.FILES.get("profile_picture"),
            emergency_contact_name=request.POST.get("emergency_contact_name"),
            emergency_contact_phone=request.POST.get("emergency_contact_phone"),
            blood_type=request.POST.get("blood_type"),
            identification_number=request.POST.get("identification_number"),
            rank=request.POST.get("rank"),
            department=request.POST.get("department"),
            unit=request.POST.get("unit"),
            badge_number=request.POST.get("badge_number"),
            service_number=request.POST.get("service_number"),
            security_clearance_level=request.POST.get("security_clearance_level"),
        )

        messages.success(request, f"MoY&S account for {user.get_full_name()} created successfully!")
        return redirect("ceate_moys_account")

    contex = {}
    return render(request, "moj_pages/admin/ceate_moys_account.html", contex)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_view_moys_account(request):
    view_moys_user = MoYS_User.objects.all().order_by('rank')
    
    context = {
        "view_moys_user": view_moys_user
    }
    return render(request, "moj_pages/admin/view_moys_account.html", context)












@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_admin_activate_deactivate_users(request):
    
    # Get only MoJ users
    moj_roles = ['moj_head', 'moj_officers', 'moj_it_head']
    users = CustomUser.objects.all()

    # Group users by role
    grouped_users = defaultdict(list)
    for user in users:
        grouped_users[user.get_role_display()].append(user)

    context = {
        "grouped_users": dict(grouped_users)
    }
    return render(request, "moj_pages/admin/activate_deactivate_users.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Prevent self-deactivation (important safeguard)
    if request.user == user:
        return redirect('activate_deactivate_users')

    user.is_active = not user.is_active
    user.save()

    return redirect('activate_deactivate_users')

@login_required(login_url='dologin')
@allowed_roles(['moj_it_head'])
def moj_admin_audit_logs(request):
    logs = UserActivityLog.objects.select_related('user').order_by('-created_at')

    # 🔍 Filters
    search = request.GET.get('search')
    action = request.GET.get('action')
    user_id = request.GET.get('user')

    if search:
        logs = logs.filter(
            Q(user__username__icontains=search) |
            Q(description__icontains=search)
        )

    if action:
        logs = logs.filter(action=action)

    if user_id:
        logs = logs.filter(user__id=user_id)

    users = CustomUser.objects.all()

    context = {
        "logs": logs,
        "users": users
    }
    return render(request, "moj_pages/admin/audit_logs.html", context)


