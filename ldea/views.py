from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.decorators import allowed_roles
from django.contrib import messages
from .models import*
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Min
from django.db.models import Sum
from django.db.models import Min, Count, Sum, F, FloatField, ExpressionWrapper, Value
from django.db.models.functions import Coalesce

import json
import time
from django.shortcuts import render
from django.db.models import Avg, Case, When, FloatField
from django.db.models.functions import ExtractYear

# Create your views here.

#===================================
#       LDEA Head Views
#===================================
@login_required(login_url='dologin')
@allowed_roles(['ldea_head'])
def ldea_head_page(request):
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

    context = {
        "effectiveness_data": json.dumps(chart_data_arrests),
        "selected_year": year,
        "years": years,
        "substance_series": json.dumps(series), 
        "drug_labels": json.dumps(drug_labels), 
        "drug_values": json.dumps(drug_values),
        "hotspot_labels": json.dumps(hotspot_labels),
        "hotspot_values": json.dumps(hotspot_values),
    }

    return render(request, "ldea_pages/ldea_head/index.html", context)

@login_required(login_url='dologin')
@allowed_roles(['ldea_head', 'moj_head'])
def ldea_trafficked_drugs_page(request):

    year = request.GET.get("year")

    seizures = Seizure.objects.select_related("drug_type").filter(
        drug_type__isnull=False
    )

    if year:
        try:
            year = int(year)
            seizures = seizures.filter(seizure_date__year=year)
        except ValueError:
            pass  # don't kill queryset

    total_seizures = seizures.count()

    trafficked_drugs = (
        seizures
        .values(
            "drug_type__id",
            "drug_type__name",
            "drug_type__photo"
        )
        .annotate(
            total_cases=Count("id"),
            total_quantity=Coalesce(Sum("quantity"), 0.0),
        )
    )

    # Add percentage AFTER annotation
    if total_seizures > 0:
        trafficked_drugs = trafficked_drugs.annotate(
            percentage=ExpressionWrapper(
                (F("total_cases") * 100.0) / total_seizures,
                output_field=FloatField()
            )
        )
    else:
        trafficked_drugs = trafficked_drugs.annotate(
            percentage=Value(0.0, output_field=FloatField())
        )

    trafficked_drugs = trafficked_drugs.order_by("-total_quantity")

    context = {
        "trafficked_drugs": trafficked_drugs,
        "total_seizures": total_seizures,
        "selected_year": year,
    }

    return render(request, "ldea_pages/ldea_head/trafficked_drugs.html", context)

@login_required(login_url='dologin')
@allowed_roles(['ldea_head', 'moj_head'])
def ldea_drug_hotspots_page(request):
    year = request.GET.get("year")

    seizures = Seizure.objects.all()

    if year:
        try:
            year = int(year)
            seizures = seizures.filter(seizure_date__year=year)
        except ValueError:
            seizures = Seizure.objects.none()

    total_seizures = seizures.count()

    # Avoid division by zero safely
    if total_seizures > 0:
        percentage_expression = ExpressionWrapper(
            (F("total_cases") * 100.0) / total_seizures,
            output_field=FloatField()
        )
    else:
        percentage_expression = Value(0.0, output_field=FloatField())

    hotspots = (
        seizures
        .values("county")
        .annotate(
            total_cases=Count("id"),
            total_quantity=Coalesce(Sum("quantity"), 0.0),
        )
        .annotate(
            percentage=percentage_expression
        )
        .order_by("-total_cases")
    )

    context = {
        "hotspots": hotspots,
        "total_seizures": total_seizures,
        "selected_year": year,
    }
    return render(request, "ldea_pages/ldea_head/drug_hotspots.html", context)

@login_required(login_url='dologin')
@allowed_roles(['ldea_head', 'moj_head'])
def ldea_new_substances_page(request):

    year = request.GET.get("year")

    seizures = Seizure.objects.select_related("drug_type").filter(
        drug_type__isnull=False
    )

    if year:
        try:
            year = int(year)
            seizures = seizures.filter(seizure_date__year=year)
        except ValueError:
            pass  # don't clear data

    # Step 1: Group + include photo
    substances = (
        seizures
        .values(
            "drug_type__id",
            "drug_type__name",
            "drug_type__photo"   # ✅ ADD THIS
        )
        .annotate(
            first_seen=Min("seizure_date"),
            total_cases=Count("id"),
            total_quantity=Coalesce(Sum("quantity"), 0.0),
        )
        .order_by("-first_seen")
    )

    total_cases_all = seizures.count()

    # Percentage
    if total_cases_all > 0:
        substances = substances.annotate(
            percentage=ExpressionWrapper(
                (F("total_cases") * 100.0) / total_cases_all,
                output_field=FloatField()
            )
        )
    else:
        substances = substances.annotate(
            percentage=Value(0.0, output_field=FloatField())
        )

    context = {
        "substances": substances,
        "total_cases": total_cases_all,
        "selected_year": year,
    }
    return render(request, "ldea_pages/ldea_head/new_substances.html", context)

#===================================
#       LDEA Head of Ops Views
#===================================
@login_required(login_url='dologin')
@allowed_roles(['ldea_ops'])
def ldea_ldea_ops_page(request):
    
    contex = {
        
    }
    return render(request, "ldea_pages/ldea_ops/index.html", contex)

@login_required(login_url='dologin')
@allowed_roles(['ldea_ops', 'ldea_head'])
def ldea_ldea_ops_active_cases(request):
    action = request.GET.get("action")
    year = request.GET.get("year")
    county = request.GET.get("county")

    cases = Cases.objects.all()

    if year:
        try:
            year = int(year)
            cases = cases.filter(created_at__year=year)
        except ValueError:
            cases = Cases.objects.none()

    if county:
        county = county.strip()
        cases = cases.filter(county__icontains=county)

    context = {
        "cases": cases,
        "selected_year": year,
        "selected_county": county,
        "action": action,
    }
    return render(request, "ldea_pages/ldea_ops/active_cases.html", context)


#===================================
#       LDEA Officers Views
#===================================
@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_page(request):
    # Count arrests per county
    county_counts = (
        Arrest.objects.values("county").annotate(total=Count("id")).order_by("-total"))

    # Convert to list for chart
    counties = [item["county"] for item in county_counts]
    totals = [item["total"] for item in county_counts]

    # Highest & Lowest
    highest = county_counts.first() if county_counts else None
    lowest = county_counts.last() if county_counts else None
    
    cases = Cases.objects.all().count()
    evidence = Evidence.objects.all().count()
    drug_raid = DrugRaid.objects.all().count()
    new_drug = DrugType.objects.all().count()
    
    
    context = {
        "counties": counties,
        "totals": totals,
        "highest": highest,
        "lowest": lowest,
        
        "cases": cases,
        "evidence": evidence,
        "drug_raid": drug_raid,
        "new_drug": new_drug,
        
    }
    return render(request, "ldea_pages/officers/index.html", context)

# ------ Arrests Person ---------
@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_ceates_arrests_person_page(request):
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", "")
        last_name = request.POST.get("last_name")
        other_name = request.POST.get("other_name", "")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        date_of_birth = request.POST.get("date_of_birth") or None
        phone_number = request.POST.get("phone_number", "")
        email = request.POST.get("email", "")
        national_id = request.POST.get("national_id", "")
        passport_number = request.POST.get("passport_number", "")
        county = request.POST.get("county", "")
        district = request.POST.get("district", "")
        address = request.POST.get("address", "")
        occupation = request.POST.get("occupation", "")
        marital_status = request.POST.get("marital_status", "")
        nationality = request.POST.get("nationality", "Liberian")
        remarks = request.POST.get("remarks", "")
        role = request.POST.get("role")
        
        drug_user = request.POST.get("drug_user")
        professional_status = request.POST.get("professional_status")
        educational_level = request.POST.get("educational_level")

        is_repeat_offender = bool(request.POST.get("is_repeat_offender"))
        is_under_investigation = bool(request.POST.get("is_under_investigation"))

        photo = request.FILES.get("photo")

        if not gender:
            messages.error(request, "Please select a gender")
            return redirect("ceate_arrests_person")

        # Save person
        person = Person.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            other_name=other_name,
            gender=gender,
            age=age,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            email=email,
            national_id=national_id,
            passport_number=passport_number,
            county=county,
            district=district,
            address=address,
            occupation=occupation,
            marital_status=marital_status,
            nationality=nationality,
            remarks=remarks,
            is_repeat_offender=is_repeat_offender,
            is_under_investigation=is_under_investigation,
            role=role,
            drug_user=drug_user,
            photo=photo,
            professional_status = professional_status,
            educational_level = educational_level, 
        )

        messages.success(request, f"{person.first_name} {person.last_name} saved successfully!")

        if role == "suspect":
            return redirect(f"{reverse('ceart_arrests')}?person_id={person.id}")

        elif role == "victim":
            return redirect(f"{reverse('create_victim_history')}?person_id={person.id}")

        else:
            return redirect("ceate_arrests_person")
            
    contex = {}
    return render(request, "ldea_pages/officers/ceates_arrests_person.html", contex)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_ceates_arrests_page(request): 
    if request.method == "POST":
        person_id = request.POST.get("person")
        arrest_date = request.POST.get("arrest_date")
        arrest_time = request.POST.get("arrest_time") or None
        county = request.POST.get("county")
        district = request.POST.get("district")
        location_description = request.POST.get("location_description")
        arresting_officer = request.POST.get("arresting_officer")
        badge_number = request.POST.get("badge_number")

        drug_type = request.POST.get("drug_type")
        quantity = request.POST.get("quantity") or None
        unit = request.POST.get("unit")

        seizure = request.POST.get("seizure")
        status = request.POST.get("status")
        charges = request.POST.get("charges")
        remarks = request.POST.get("remarks")

        # Get related objects
        person = Person.objects.get(id=person_id)
        
        # Save arrest
        Arrest.objects.create(
            person=person,
            arrest_date=arrest_date,
            arrest_time=arrest_time,
            county=county,
            district=district,
            location_description=location_description,
            arresting_officer=arresting_officer,
            badge_number=badge_number,
            drug_type=drug_type,
            quantity=quantity,
            unit=unit,
            seizure=seizure,
            status=status,
            charges=charges,
            remarks=remarks
        )

        messages.success(request, "Arrest saved successfully!")
        return redirect("ceate_arrests_person")

    # GET request
    persons = Person.objects.all()
    drug_types = DrugType.objects.all()
    seizures = Seizure.objects.all()
    selected_person_id = request.GET.get("person_id")

    context = {
        "persons": persons,
        "drug_types": drug_types,
        "seizures": seizures,
        "selected_person_id": selected_person_id,
    }
    return render(request, "ldea_pages/officers/ceates_arrests.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers', 'moh_officers', 'moh_head'])
def ldea_ceates_victim_history(request):
    saved_person_ids = VictimHistory.objects.values_list("person_id", flat=True)
    persons = Person.objects.filter(role="victim").exclude(id__in=saved_person_ids)

    selected_person_id = request.GET.get("person_id")

    if request.method == "POST":
        person = get_object_or_404(Person, id=request.POST.get("person_id"))

        VictimHistory.objects.create(

            # =========================
            # PERSON + INCIDENT
            # =========================
            person=person,
            incident_date=request.POST.get("incident_date"),
            incident_time=request.POST.get("incident_time") or None,
            incident_location=request.POST.get("incident_location"),

            # =========================
            # DRUG INFO
            # =========================
            primary_substance=request.POST.get("primary_substance"),
            secondary_substances=request.POST.get("secondary_substances"),
            type_of_drug_used=request.POST.get("type_of_drug_used"),

            frequency_of_use=request.POST.get("frequency_of_use"),
            last_used_date=request.POST.get("last_used_date") or None,
            age_first_used=request.POST.get("age_first_used"),
            duration_of_addiction_years=request.POST.get("duration_of_addiction_years") or None,

            method_of_use=request.POST.get("method_of_use"),
            dependency_level=request.POST.get("dependency_level"),

            overdose_history=request.POST.get("overdose_history"),
            overdose_count=request.POST.get("overdose_count"),

            mental_health_issues=request.POST.get("mental_health_issues"),

            rehab_history=request.POST.get("rehab_history"),
            if_rehab_yes=request.POST.get("if_rehab_yes"),

            arrest_reference=request.POST.get("arrest_reference"),
        )
        messages.success(request, "Victim History saved successfully!")
        if request.user.role == "moh_officers":
            return redirect("create_beneficial")

        elif request.user.role == "officers":
            return redirect("ceate_arrests_person")

    context = {
        "persons": persons,
        "selected_person_id": selected_person_id
    }
    return render(request, "ldea_pages/officers/ceates_victim_history.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers', 'ldea_head', 'moh_officers', 'moh_head'])
def ldea_officers_arrests_person_detail(request, id):
    
    person = get_object_or_404(Person, id=id)

    # If suspect → arrests
    arrests = None
    if person.role == "suspect":
        arrests = person.arrests.all().order_by("-arrest_date")

    # If victim → victim history
    victim_history = None
    if person.role == "victim":
        victim_history = person.victim.all().order_by("-incident_date")

    context = {
        "person": person,
        "arrests": arrests,
        "victim_history": victim_history,
    }
    return render(request, "ldea_pages/officers/arrests_person_detail.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers', 'ldea_head', 'moh_officers', 'moh_head'])
def ldea_view_arrests_person_page(request):
    action = request.GET.get("action")

    # Always start with queryset
    persons = Person.objects.all().order_by('-created_at')

    year = request.GET.get("year")
    county = request.GET.get("county")
    role = request.GET.get("role")

    # APPLY FILTERS
    if year:
        persons = persons.filter(created_at__year=year)

    if county:
        persons = persons.filter(county=county)

    if role:
        persons = persons.filter(role=role)

    # Keep ordering after filters
    persons = persons.order_by('-created_at')

    # TITLE LOGIC
    if role == "victim":
        page_title = "View Victim Records"
    elif role == "suspect":
        page_title = "View Arrest Records"
    else:
        page_title = "View Persons Records"

    context = {
        "action": action,
        "persons": persons,
        "selected_year": year,
        "selected_county": county,
        "selected_role": role,
        "page_title": page_title,
    }
    return render(request, "ldea_pages/officers/view_arrests_person.html", context)

# LDEA Officers Create and view Cases
@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_create_cases(request):

    # =====================================
    # GET SAVED SUSPECT IDS
    # =====================================
    saved_suspects = CaseParticipant.objects.filter(
        role="suspect"
    ).values_list("person_id", flat=True)

    # =====================================
    # GET PERSONS THAT ARE NOT SAVED
    # =====================================
    persons = Person.objects.exclude(
        id__in=saved_suspects
    )

    if request.method == "POST":

        case_number = request.POST.get("case_number")

        # =====================================
        # CHECK DUPLICATE CASE NUMBER
        # =====================================
        if Cases.objects.filter(case_number=case_number).exists():

            messages.error(
                request,
                "Case Number already exists."
            )

            return render(
                request,
                "ldea_pages/officers/create_cases.html",
                {
                    "persons": persons,
                }
            )

        title = request.POST.get("title")
        description = request.POST.get("description")
        court_name = request.POST.get("court_name")
        status = request.POST.get("status")

        action_taken = request.POST.get("action_taken")
        substance = request.POST.get("substance")
        charge = request.POST.get("charge")
        county = request.POST.get("county")

        # =====================================
        # CREATE CASE
        # =====================================
        case = Cases.objects.create(
            case_number=case_number,
            title=title,
            description=description,
            court_name=court_name,
            action_taken=action_taken,
            substance=substance,
            charge=charge,
            county=county,
            status=status or "pending",
        )

        # =====================================
        # SUSPECTS
        # =====================================
        suspect_ids = request.POST.getlist("suspect_ids[]")
        primary_suspect_index = request.POST.get("primary_suspect")

        for index, person_id in enumerate(suspect_ids):

            # SKIP EMPTY VALUES
            if not person_id or person_id == "Select Suspect":
                continue

            try:
                person = Person.objects.get(id=person_id)

                is_primary = (
                    str(index) == str(primary_suspect_index)
                )

                CaseParticipant.objects.create(
                    case=case,
                    person=person,
                    role="suspect",
                    is_primary=is_primary
                )

            except Person.DoesNotExist:
                continue

        # =====================================
        # VICTIMS
        # =====================================
        victim_ids = request.POST.getlist("victim_ids[]")
        primary_victim_index = request.POST.get("primary_victim")

        for index, person_id in enumerate(victim_ids):

            # SKIP EMPTY VALUES
            if not person_id or person_id == "Select Victim":
                continue

            try:
                person = Person.objects.get(id=person_id)

                is_primary = (
                    str(index) == str(primary_victim_index)
                )

                CaseParticipant.objects.create(
                    case=case,
                    person=person,
                    role="victim",
                    is_primary=is_primary
                )

            except Person.DoesNotExist:
                continue

        messages.success(
            request,
            "Case created successfully!"
        )

        return redirect("create_case")

    context = {
        "persons": persons,
    }
    return render(request, "ldea_pages/officers/create_cases.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_view_cases(request):
    action = request.GET.get("action")
    year = request.GET.get("year")

    cases_by_month = []

    # Base queryset
    cases = Cases.objects.all()
    case_participants = CaseParticipant.objects.all()

    if year:
        try:
            year_int = int(year)

            # Filter cases by year
            cases = cases.filter(created_at__year=year_int)

            # Filter participants linked to those cases
            case_participants = case_participants.filter(case__in=cases)

            # Group by month
            cases_by_month = cases.annotate(
                month_num=ExtractMonth('created_at')
            ).order_by('-month_num')

        except ValueError:
            cases = Cases.objects.none()
            case_participants = CaseParticipant.objects.none()
            cases_by_month = []

    context = {
        "action": action,
        "view_cases": cases_by_month,
        "participants": case_participants,
        "year": year,
    }

    return render(request, "ldea_pages/officers/view_cases.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers', 'ldea_ops', 'ldea_head'])
def ldea_officers_cases_detail(request, id):
    case = get_object_or_404(Cases, id=id)

    participants = case.participants.select_related("person").all()

    # Filter using PERSON role (NOT CaseParticipant.role)
    suspects = [p for p in participants if p.person.role == "suspect"]
    victims = [p for p in participants if p.person.role == "victim"]
    witnesses = [p for p in participants if p.person.role == "witness"]

    charges_list = case.charge.split(",") if case.charge else []

    evidence_list = []
    if case.substance:
        evidence_list = [e.strip() for e in case.substance.split(",")]

    context = {
        "case": case,
        "participants": participants,
        "suspects": suspects,
        "victims": victims,
        "witnesses": witnesses,
        "charges_list": charges_list,
        "evidence_list": evidence_list,
    }
    return render(request, "ldea_pages/officers/cases_detail.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_edit_cases(request, id):
    
    case = get_object_or_404(Cases, id=id)

    if request.method == "POST":

        # =========================
        # UPDATE CASE FIELDS
        # =========================
        case.case_number = request.POST.get("case_number")
        case.title = request.POST.get("title")
        case.description = request.POST.get("description")
        case.court_name = request.POST.get("court_name")
        case.status = request.POST.get("status")
        case.action_taken = request.POST.get("action_taken")
        case.substance = request.POST.get("substance")
        case.charge = request.POST.get("charge")
        case.county = request.POST.get("county")

        case.save()

        # =========================
        # REMOVE OLD PARTICIPANTS
        # =========================
        CaseParticipant.objects.filter(case=case).delete()

        # =========================
        # RE-ADD SUSPECTS
        # =========================
        suspect_ids = request.POST.getlist("suspect_ids[]")
        primary_suspect_index = request.POST.get("primary_suspect")

        for index, person_id in enumerate(suspect_ids):

            if not person_id:
                continue

            person = Person.objects.get(id=person_id)

            CaseParticipant.objects.create(
                case=case,
                person=person,
                role="suspect",
                is_primary=(str(index) == str(primary_suspect_index))
            )

        messages.success(request, "Case updated successfully!")
        return redirect("edit_cases", id=case.id)

    # =========================
    # LOAD EXISTING DATA
    # =========================
    selected_suspects = CaseParticipant.objects.filter(
        case=case,
        role="suspect"
    ).values_list("person_id", flat=True)

    persons = Person.objects.filter(role="suspect")

    context = {
        "case": case,
        "persons": persons,
        "selected_suspects": list(selected_suspects),
    }
    return render(request, "ldea_pages/officers/edit_cases.html", context)

# LDEA Officers Create and view Evidence
@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_create_evidence(request):
    if request.method == "POST":
        name = request.POST.get("name")
        evidence_type = request.POST.get("evidence_type")
        status = request.POST.get("status")

        quantity = request.POST.get("quantity") or None
        unit = request.POST.get("unit")

        drug_type_id = request.POST.get("drug_type")
        arrest_id = request.POST.get("arrest")
        case_id = request.POST.get("case")

        county = request.POST.get("county")
        district = request.POST.get("district")
        location_description = request.POST.get("location_description")

        collected_by = request.POST.get("collected_by")
        badge_number = request.POST.get("badge_number")

        remarks = request.POST.get("remarks")

        # Relations
        drug_type = DrugType.objects.get(id=drug_type_id) if drug_type_id else None
        arrest = Arrest.objects.get(id=arrest_id) if arrest_id else None
        case = Cases.objects.get(id=case_id) if case_id else None

        # Save
        Evidence.objects.create(
            name=name,
            evidence_type=evidence_type,
            status=status,
            quantity=quantity,
            unit=unit,
            drug_type=drug_type,
            arrest=arrest,
            case=case,
            county=county,
            district=district,
            location_description=location_description,
            collected_by=collected_by,
            badge_number=badge_number,
            remarks=remarks
        )

        messages.success(request, "Evidence saved successfully!")
        return redirect("create_evidence")
        
    used_arrests = Evidence.objects.exclude(arrest__isnull=True).values_list("arrest_id", flat=True)
    used_cases = Evidence.objects.exclude(case__isnull=True).values_list("case_id", flat=True)

    context = {
        "drug_types": DrugType.objects.all(),
        "arrests": Arrest.objects.exclude(id__in=used_arrests),
        "cases": Cases.objects.exclude(id__in=used_cases),
    }
    return render(request, "ldea_pages/officers/create_evidence.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_edit_evidence(request, id):
    evidence = get_object_or_404(Evidence, id=id)

    if request.method == "POST":

        evidence.name = request.POST.get("name")
        evidence.evidence_type = request.POST.get("evidence_type")
        evidence.status = request.POST.get("status")

        evidence.quantity = request.POST.get("quantity") or None
        evidence.unit = request.POST.get("unit")

        drug_type_id = request.POST.get("drug_type")
        arrest_id = request.POST.get("arrest")
        case_id = request.POST.get("case")

        evidence.county = request.POST.get("county")
        evidence.district = request.POST.get("district")
        evidence.location_description = request.POST.get("location_description")

        evidence.collected_by = request.POST.get("collected_by")
        evidence.badge_number = request.POST.get("badge_number")

        evidence.remarks = request.POST.get("remarks")

        # Relations
        evidence.drug_type = DrugType.objects.get(id=drug_type_id) if drug_type_id else None
        evidence.arrest = Arrest.objects.get(id=arrest_id) if arrest_id else None
        evidence.case = Cases.objects.get(id=case_id) if case_id else None

        evidence.save()

        messages.success(request, "Evidence updated successfully!")
        return redirect("edit_evidence", id=evidence.id)

    context = {
        "evidence": evidence,
        "drug_types": DrugType.objects.all(),
        "arrests": Arrest.objects.all(),
        "cases": Cases.objects.all(),
    }
    return render(request, "ldea_pages/officers/edit_evidence.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_view_evidence(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    evidences = Evidence.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        evidences = evidences.filter(created_at__year=year)

    # Filter by county
    if county:
        evidences = evidences.filter(county__iexact=county)

    context = {
        "action": action,
        "evidences": evidences,
        "year": year,
        "county": county,
    }
    return render(request, "ldea_pages/officers/view_evidence.html", context)

# ---- Create and View Drug Raid -----
@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_crate_drug_raid(request):
    view_officers = LDEA_User.objects.all()

    if request.method == "POST":

        lead_officer = get_object_or_404(
            LDEA_User,
            id=request.POST.get("lead_officer")
        )

        raid = DrugRaid.objects.create(
            title=request.POST.get("title"),
            location=request.POST.get("location"),
            city=request.POST.get("city"),
            county=request.POST.get("county"),
            raid_date=request.POST.get("raid_date"),
            raid_time=request.POST.get("raid_time") or None,
            status=request.POST.get("status"),
            description=request.POST.get("description"),
            lead_officer=lead_officer,
            total_arrests=int(request.POST.get("total_arrests") or 0),
            total_seizures=int(request.POST.get("total_seizures") or 0),
            created_by=request.user
        )

        # team members
        raid.team_members.set(request.POST.getlist("team_members"))

        messages.success(request, "Drug raid created successfully!")
        return redirect("crate_drug_raid")

    context = {
        "view_officers": view_officers,
    }
    return render(request, "ldea_pages/officers/create_drug_raid.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers', 'ldea_ops'])
def ldea_officers_view_drug_raid(request):
    action = request.GET.get("action")
    year = request.GET.get("year")
    county = request.GET.get("county")

    raids_by_month = []

    # Base queryset
    view_new_drug = DrugRaid.objects.all()

    # Filter by year
    if year:
        try:
            year_int = int(year)
            view_new_drug = view_new_drug.filter(raid_date__year=year_int)
        except ValueError:
            view_new_drug = DrugRaid.objects.none()

    # Filter by county
    if county:
        view_new_drug = view_new_drug.filter(county__iexact=county)

    # Group / annotate by month
    if view_new_drug.exists():
        raids_by_month = view_new_drug.annotate(
            month_num=ExtractMonth('raid_date')
        ).order_by('month_num')

    context = {
        "action": action,
        "view_new_drug": raids_by_month,
        "year": year,
        "county": county,
    }
    return render(request, "ldea_pages/officers/view_drug_raid.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers', 'ldea_ops'])
def ldea_officers_edit_drug_raid(request, id):
    raid = get_object_or_404(DrugRaid, id=id)

    # FIXED
    officers = LDEA_User.objects.all()

    if request.method == "POST":

        raid.title = request.POST.get("title")
        raid.reference_code = request.POST.get("reference_code")
        raid.location = request.POST.get("location")
        raid.city = request.POST.get("city")
        raid.county = request.POST.get("county")
        raid.raid_date = request.POST.get("raid_date")
        raid.raid_time = request.POST.get("raid_time")

        raid.total_arrests = request.POST.get("total_arrests") or 0
        raid.total_seizures = request.POST.get("total_seizures") or 0

        raid.status = request.POST.get("status")
        raid.description = request.POST.get("description")

        # =========================
        # LEAD OFFICER
        # =========================
        lead_officer_id = request.POST.get("lead_officer")

        if lead_officer_id:
            raid.lead_officer_id = lead_officer_id

        raid.save()

        # =========================
        # TEAM MEMBERS
        # =========================
        team_members = request.POST.getlist("team_members")

        raid.team_members.set(team_members)

        messages.success(request, "Drug raid updated successfully!")

        return redirect("edit_drug_raid", id=raid.id)

    context = {
        "raid": raid,
        "view_officers": officers,
        "selected_team": raid.team_members.values_list("id", flat=True),
    }
    return render(request, "ldea_pages/officers/edit_drug_raid.html", context)

# LDEA Officers Ceate and view Seizure
@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_create_seizure(request):
    drug_types = DrugType.objects.all()
    
    if request.method == "POST":
        drug_type_id = request.POST.get("drug_type")

        Seizure.objects.create(
            seizure_date=request.POST.get("seizure_date"),
            seizure_time=request.POST.get("seizure_time") or None,
            county=request.POST.get("county"),
            district=request.POST.get("district"),
            location_description=request.POST.get("location_description"),
            seized_by=request.POST.get("seized_by"),
            badge_number=request.POST.get("badge_number"),
            drug_type_id=drug_type_id if drug_type_id else None,
            quantity=request.POST.get("quantity") or None,
            unit=request.POST.get("unit"),
            photo=request.FILES.get("photo"),
            status=request.POST.get("status"),
            remarks=request.POST.get("remarks"),
        )

        messages.success(request, "Seizure recorded successfully")
        return redirect("crate_drug_seizure")
    
    context = {
       "drug_types": drug_types
    }
    return render(request, "ldea_pages/officers/create_seizure.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers', 'moj_head', 'ldea_head'])
def ldea_officers_view_seizure(request):
    action = request.GET.get("action")
    year = request.GET.get("year")
    county = request.GET.get("county")

    seizures = Seizure.objects.all()

    # =========================
    # FILTER BY YEAR
    # =========================
    if year:
        try:
            year_int = int(year)
            seizures = seizures.filter(seizure_date__year=year_int)
        except ValueError:
            seizures = Seizure.objects.none()

    # =========================
    # FILTER BY COUNTY
    # =========================
    if county:
        seizures = seizures.filter(county__iexact=county)

    # =========================
    # ORDER / GROUP
    # =========================
    seizures = seizures.annotate(
        month_num=ExtractMonth('seizure_date')
    ).order_by('-seizure_date')

    context = {
        "view_seizures": seizures,
        "year": year,
        "county": county,
        "action": action,
    }
    return render(request, "ldea_pages/officers/view_seizure.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_edit_drug_seizure(request, id):
    seizure = get_object_or_404(Seizure, id=id)

    if request.method == "POST":

        # UPDATE BASIC FIELDS
        seizure.seizure_date = request.POST.get("seizure_date")
        seizure.seizure_time = request.POST.get("seizure_time")

        seizure.county = request.POST.get("county")
        seizure.district = request.POST.get("district")
        seizure.location_description = request.POST.get("location_description")

        seizure.seized_by = request.POST.get("seized_by")
        seizure.badge_number = request.POST.get("badge_number")

        seizure.quantity = request.POST.get("quantity") or None
        seizure.unit = request.POST.get("unit")

        seizure.status = request.POST.get("status")
        seizure.remarks = request.POST.get("remarks")

        # FOREIGN KEY (Drug Type)
        drug_type_id = request.POST.get("drug_type")
        if drug_type_id:
            seizure.drug_type_id = drug_type_id

        # IMAGE UPDATE
        if request.FILES.get("photo"):
            seizure.photo = request.FILES.get("photo")

        seizure.save()

        messages.success(request, "Seizure updated successfully!")
        return redirect("edit_drug_seizure", id=seizure.id)

    context = {
        "seizure": seizure,
        "drug_types": DrugType.objects.all(),
    }
    return render(request, "ldea_pages/officers/edit_seizure.html", context)

# ------ Create New Drug and view ------
@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_login_new_drug(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        common_units = request.POST.get("common_units")
        description = request.POST.get("description")
        photo=request.FILES.get("photo")

        # Check if drug already exists
        if DrugType.objects.filter(name=name).exists():
            messages.error(request, "Drug already exists!")
        else:
            DrugType.objects.create(
                name=name,
                category=category,
                common_units=common_units,
                description=description,
                photo=photo,
                added_by=request.user 
            )
            messages.success(request, "Drug created successfully!")
            return redirect("crate_new_drug")  # reload page

    context = {}
    return render(request, "ldea_pages/officers/create_new_drug.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_view_new_drug(request):
    view_new_drug = DrugType.objects.all().order_by("-id")
    
    context = {
      "view_new_drug": view_new_drug,  
    }
    return render(request, "ldea_pages/officers/view_new_drug.html", context)

@login_required(login_url='dologin')
@allowed_roles(['officers'])
def ldea_officers_edit_new_drug(request, id):
    drug = get_object_or_404(DrugType, id=id)

    if request.method == "POST":

        drug.name = request.POST.get("name")
        drug.category = request.POST.get("category")
        drug.common_units = request.POST.get("common_units")
        drug.description = request.POST.get("description")

        # update image only if new file uploaded
        if request.FILES.get("photo"):
            drug.photo = request.FILES.get("photo")

        drug.save()

        messages.success(request, "Drug updated successfully!")
        return redirect("edit_new_drug", id=drug.id)

    context = {
        "drug": drug
    }
    return render(request, "ldea_pages/officers/edit_new_drug.html", context)










