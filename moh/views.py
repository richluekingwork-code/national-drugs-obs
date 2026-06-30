from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.decorators import allowed_roles
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import*
from mog.models import*
from .models import*
from ldea.models import*
import json
from django.db.models import Count
 


# Create your views here.
#===================================
#       MoH Head Views
#===================================
@login_required(login_url='dologin')
@allowed_roles(['moh_head'])
def moh_head_home(request):
    # ---------------------------
    # 1. Gender counts
    # ---------------------------
    male_count = Person.objects.filter(gender="male").count()
    female_count = Person.objects.filter(gender="female").count()
    other_count = Person.objects.filter(gender="other").count()

    # ---------------------------
    # 2. DemandReduction by type_of_treatment
    # ---------------------------
    treatment_queryset = (
        DemandReduction.objects
        .values("type_of_treatment")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    treatment_labels = []
    treatment_totals = []

    for row in treatment_queryset:
        label = row["type_of_treatment"] or "Unknown"
        treatment_labels.append(label)
        treatment_totals.append(row["total"])

    # fallback if empty
    if not treatment_labels:
        treatment_labels = ["No Data"]
        treatment_totals = [0]

    # ---------------------------
    # 2. DemandReduction by county
    # ---------------------------
    county_queryset = (
        DemandReduction.objects
        .values("county")
        .annotate(total=Count("id"))
    )

    # Convert to list and clean nulls
    county_list = [
        {
            "county": row["county"] or "Unknown",
            "total": row["total"]
        }
        for row in county_queryset
    ]

    # ---------------------------
    # 3. Get highest & lowest
    # ---------------------------
    highest = max(county_list, key=lambda x: x["total"], default=None)
    lowest = min(county_list, key=lambda x: x["total"], default=None)

    # Prepare chart data
    hl_counties = []
    hl_totals = []

    if highest:
        hl_counties.append(f"Highest: {highest['county']}")
        hl_totals.append(highest["total"])

    if lowest:
        hl_counties.append(f"Lowest: {lowest['county']}")
        hl_totals.append(lowest["total"])

    # fallback if no data
    if not hl_counties:
        hl_counties = ["No Data"]
        hl_totals = [0]
        
    # ---------------------------
    # Prevention by County
    # ---------------------------
    prevention_county_queryset = (
        Prevention.objects
        .values("county")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    prevention_county_labels = []
    prevention_county_totals = []

    for row in prevention_county_queryset:
        prevention_county_labels.append(row["county"] or "Unknown")
        prevention_county_totals.append(row["total"])

    # Fallback if no data
    if not prevention_county_labels:
        prevention_county_labels = ["No Data"]
        prevention_county_totals = [0]
    data = DemandReduction.objects.values("county").annotate(total=Count("id"))

    counties = [d["county"] for d in data]
    totals = [d["total"] for d in data]
    
    # Treatment Facilities by County
    facility_county_queryset = (
        TreatmentFacility.objects
        .values("county")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    facility_county_labels = []
    facility_county_totals = []

    for row in facility_county_queryset:
        facility_county_labels.append(row["county"] or "Unknown")
        facility_county_totals.append(row["total"])

    if not facility_county_labels:
        facility_county_labels = ["No Data"]
        facility_county_totals = [0]

    context = {
        "counties": counties,
        "totals": totals,
   
        "male_count": male_count,
        "female_count": female_count,
        "other_count": other_count,

        "prevention_county_labels": prevention_county_labels,
        "prevention_county_totals": prevention_county_totals,

        "hl_counties": hl_counties,
        "hl_totals": hl_totals,
        
        "treatment_labels": treatment_labels,
        "treatment_totals": treatment_totals,
        
        "facility_county_labels": facility_county_labels,
        "facility_county_totals": facility_county_totals,
    }
    return render(request, "moh_pages/head/index.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_head'])
def moh_view_chat_report(request):
    # Demand Reduction by County
    demand_county_data = (DemandReduction.objects.values('county').annotate(total=Count('id')).order_by('county'))
    demand_counties = [i['county'] or 'Unknown' for i in demand_county_data]
    demand_totals = [i['total'] for i in demand_county_data]

    # Prevention by County
    prevention_county_data = (Prevention.objects.values('county').annotate(total=Count('id')).order_by('county'))
    prevention_counties = [i['county'] or 'Unknown' for i in prevention_county_data]
    prevention_totals = [i['total'] for i in prevention_county_data]

    # Treatment Facility by County
    facility_data = (TreatmentFacility.objects.values('county').annotate(total=Count('id')).order_by('county'))
    facility_counties = [i['county'] or 'Unknown' for i in facility_data]
    facility_totals = [i['total'] for i in facility_data]

    # Child & Adult Assessments
    assessment_data = (ChildAdultAssessments.objects.values('county').annotate(total=Count('id')).order_by('county'))
    assessment_counties = [i['county'] or 'Unknown' for i in assessment_data]
    assessment_totals = [i['total'] for i in assessment_data]
    
    # Beneficiary Verification (IMPORTANT: use follow_county OR county field)
    verification_data = (BeneficiaryVerification.objects.values('follow_county').annotate(total=Count('id')).order_by('follow_county'))
    verification_counties = [i['follow_county'] or 'Unknown' for i in verification_data]
    verification_totals = [i['total'] for i in verification_data]
    
    # Beneficiary Handover by County
    handover_data = (BeneficiaryHandover.objects.values('follow_county').annotate(total=Count('id')).order_by('follow_county'))
    handover_counties = [i['follow_county'] or 'Unknown' for i in handover_data]
    handover_totals = [i['total'] for i in handover_data]
    
    # Case Closure by County (follow_county)
    caseclosure_data = (CaseClosure.objects.values('follow_county').annotate(total=Count('id')).order_by('follow_county'))
    caseclosure_counties = [i['follow_county'] or 'Unknown' for i in caseclosure_data]
    caseclosure_totals = [i['total'] for i in caseclosure_data]
    
    context = {
        'counties': json.dumps(demand_counties),
        'totals': json.dumps(demand_totals),

        'prevention_counties': json.dumps(prevention_counties),
        'prevention_totals': json.dumps(prevention_totals),

        'facility_counties': json.dumps(facility_counties),
        'facility_totals': json.dumps(facility_totals),
        
        'assessment_counties': json.dumps(assessment_counties),
        'assessment_totals': json.dumps(assessment_totals),
        
        'verification_counties': json.dumps(verification_counties),
        'verification_totals': json.dumps(verification_totals),
        
        'handover_counties': json.dumps(handover_counties),
        'handover_totals': json.dumps(handover_totals),
         
        'caseclosure_counties': json.dumps(caseclosure_counties),
        'caseclosure_totals': json.dumps(caseclosure_totals),
    }
    return render(request, "moh_pages/head/view_chat_report.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_head'])
def moh_view_detail_report(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    person_detail = Person.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        person_detail = person_detail.filter(created_at__year=year)

    # Filter by county
    if county:
        person_detail = person_detail.filter(county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "person_detail": person_detail,
    }
    return render(request, "moh_pages/head/view_detail_report.html", context)

def moh_detail_report(request, id):
    
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
    return render(request, "moh_pages/head/detail_report.html", context)

#===================================
#       MoH Officers Views
#===================================
@login_required(login_url='dologin')
@allowed_roles(['moh_officers'])
def moh_officers_home(request):
    # ---------------------------
    # 1. Gender counts
    # ---------------------------
    male_count = Person.objects.filter(gender="male").count()
    female_count = Person.objects.filter(gender="female").count()
    other_count = Person.objects.filter(gender="other").count()

    # ---------------------------
    # 2. DemandReduction by type_of_treatment
    # ---------------------------
    treatment_queryset = (
        DemandReduction.objects
        .values("type_of_treatment")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    treatment_labels = []
    treatment_totals = []

    for row in treatment_queryset:
        label = row["type_of_treatment"] or "Unknown"
        treatment_labels.append(label)
        treatment_totals.append(row["total"])

    # fallback if empty
    if not treatment_labels:
        treatment_labels = ["No Data"]
        treatment_totals = [0]

    # ---------------------------
    # 2. DemandReduction by county
    # ---------------------------
    county_queryset = (
        DemandReduction.objects
        .values("county")
        .annotate(total=Count("id"))
    )

    # Convert to list and clean nulls
    county_list = [
        {
            "county": row["county"] or "Unknown",
            "total": row["total"]
        }
        for row in county_queryset
    ]

    # ---------------------------
    # 3. Get highest & lowest
    # ---------------------------
    highest = max(county_list, key=lambda x: x["total"], default=None)
    lowest = min(county_list, key=lambda x: x["total"], default=None)

    # Prepare chart data
    hl_counties = []
    hl_totals = []

    if highest:
        hl_counties.append(f"Highest: {highest['county']}")
        hl_totals.append(highest["total"])

    if lowest:
        hl_counties.append(f"Lowest: {lowest['county']}")
        hl_totals.append(lowest["total"])

    # fallback if no data
    if not hl_counties:
        hl_counties = ["No Data"]
        hl_totals = [0]
        
    # ---------------------------
    # Prevention by County
    # ---------------------------
    prevention_county_queryset = (
        Prevention.objects
        .values("county")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    prevention_county_labels = []
    prevention_county_totals = []

    for row in prevention_county_queryset:
        prevention_county_labels.append(row["county"] or "Unknown")
        prevention_county_totals.append(row["total"])

    # Fallback if no data
    if not prevention_county_labels:
        prevention_county_labels = ["No Data"]
        prevention_county_totals = [0]
    data = DemandReduction.objects.values("county").annotate(total=Count("id"))

    counties = [d["county"] for d in data]
    totals = [d["total"] for d in data]

    context = {
        "counties": counties,
        "totals": totals,
   
        "male_count": male_count,
        "female_count": female_count,
        "other_count": other_count,

        "prevention_county_labels": prevention_county_labels,
        "prevention_county_totals": prevention_county_totals,

        "hl_counties": hl_counties,
        "hl_totals": hl_totals,
        
        "treatment_labels": treatment_labels,
        "treatment_totals": treatment_totals,
    }
    return render(request, "moh_pages/officers/index.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers'])
def moh_officers_create_beneficial(request):
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        other_name = request.POST.get("other_name")

        gender = request.POST.get("gender")
        age = request.POST.get("age")
        date_of_birth = request.POST.get("date_of_birth")

        marital_status = request.POST.get("marital_status")
        educational_level = request.POST.get("educational_level")
        professional_status = request.POST.get("professional_status")

        phone_number = request.POST.get("phone_number")
        county = request.POST.get("county")
        district = request.POST.get("district")
        nationality = request.POST.get("nationality")
        address = request.POST.get("address")

        role = request.POST.get("role")

        # File upload
        photo = request.FILES.get("photo")

        # Save to database
        person = Person.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            other_name=other_name,
            gender=gender,
            age=age,
            date_of_birth=date_of_birth,
            marital_status=marital_status,
            educational_level=educational_level,
            professional_status=professional_status,
            phone_number=phone_number,
            county=county,
            district=district,
            nationality=nationality,
            address=address,
            role=role,
            photo=photo
        )

        # Optional: redirect after save
        messages.success(request, f"{person.first_name} {person.last_name} saved successfully!")
        return redirect(
            f"{reverse('create_victim_history')}?person_id={person.id}"
        )
        
    context = {
       
    }
    return render(request, "moh_pages/officers/create_beneficial.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers'])
def moh_officers_demand_reduction(request):
    
    used_person_ids = DemandReduction.objects.values_list('persons', flat=True)
    get_persons = Person.objects.filter(role='victim').exclude(id__in=used_person_ids)
    
    if request.method == "POST":

        # MANY TO MANY
        persons_ids = request.POST.getlist("persons[]")

        # MULTIPLE SELECTS (IMPORTANT FIX)
        treatment = ", ".join(request.POST.getlist("treatment"))
        drug_test = ", ".join(request.POST.getlist("drug_test"))
        type_of_treatment = ", ".join(request.POST.getlist("type_of_treatment"))
        psychotherapeutic_intervention = ", ".join(request.POST.getlist("psychotherapeutic_intervention"))
        psychotropic_interventions = ", ".join(request.POST.getlist("psychotropic_interventions"))
        route_of_administration = ", ".join(request.POST.getlist("route_of_administration"))

        # SINGLE FIELDS
        cases = request.POST.get("cases")
        injection_substance = request.POST.get("injection_substance")

        county = request.POST.get("county")
        city = request.POST.get("city")
        district = request.POST.get("district")

        treatment_facility = request.POST.get("treatment_facility")
        comorbid_conditions = request.POST.get("comorbid_conditions")
        refer_from = request.POST.get("refer_from")
        admission_status = request.POST.get("admission_status")
        refer_to = request.POST.get("refer_to")

        # CREATE OBJECT
        demand = DemandReduction.objects.create(
            treatment=treatment,
            cases=cases,
            injection_substance=injection_substance,
            drug_test=drug_test,

            county=county,
            city=city,
            district=district,

            treatment_facility=treatment_facility,
            type_of_treatment=type_of_treatment,

            psychotherapeutic_intervention=psychotherapeutic_intervention,
            psychotropic_interventions=psychotropic_interventions,
            comorbid_conditions=comorbid_conditions,
            route_of_administration=route_of_administration,
            refer_from=refer_from,
            admission_status=admission_status,
            refer_to=refer_to,
        )

        # MANY TO MANY SAVE
        demand.persons.set(persons_ids)

        messages.success(request, "Demand Reduction record saved successfully!")
        return redirect("demand_reduction")
    
    context = { 
       "get_persons": get_persons,
    }
    return render(request, "moh_pages/officers/demand_reduction.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers', 'moh_head'])
def moh_officers_view_demand_reduction(request):
    action = request.GET.get("action")
    year = request.GET.get("year")
    county = request.GET.get("county")

    demands = DemandReduction.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        try:
            year_int = int(year)
            demands = demands.filter(created_at__year=year_int)
        except ValueError:
            demands = DemandReduction.objects.none()

    # Filter by county
    if county:
        demands = demands.filter(county__iexact=county)

    context = {
        "action": action,
        "demands": demands,
        "year": year,
        "county": county,
    }
    return render(request, "moh_pages/officers/view_demand_reduction.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers', 'moh_head'])
def moh_officers_demand_reduction_detail(request, id):
    demand = get_object_or_404(DemandReduction.objects.prefetch_related("persons"), id=id)

    context = {
        "demand": demand
    }
    return render(request, "moh_pages/officers/demand_reduction_datile.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers'])
def moh_officers_creat_prevention(request):
    if request.method == "POST":

        institution_name = request.POST.get("institution_name")
        address = request.POST.get("address")
        date = request.POST.get("date")

        district = request.POST.get("district")
        county = request.POST.get("county")

        # BOOLEAN CHECKBOXES (IMPORTANT FIX)
        sud_awareness = request.POST.get("sud_awareness") == "on"
        school_health_club = request.POST.get("school_health_club") == "on"
        media_campaign = request.POST.get("media_campaign") == "on"
        harm_reduction = request.POST.get("harm_reduction") == "on"
        radio_talk_show = request.POST.get("radio_talk_show") == "on"

        # TEXT AREAS
        sud_communities = request.POST.get("sud_communities", "")
        school_names = request.POST.get("school_names", "")
        media_details = request.POST.get("media_details", "")
        harm_reduction_details = request.POST.get("harm_reduction_details", "")
        radio_details = request.POST.get("radio_details", "")

        # SAVE TO DB
        Prevention.objects.create(
            institution_name=institution_name,
            address=address,
            date=date,
            district=district,
            county=county,

            sud_awareness=sud_awareness,
            sud_communities=sud_communities,

            school_health_club=school_health_club,
            school_names=school_names,

            media_campaign=media_campaign,
            media_details=media_details,

            harm_reduction=harm_reduction,
            harm_reduction_details=harm_reduction_details,

            radio_talk_show=radio_talk_show,
            radio_details=radio_details,
        )

        messages.success(request, "Prevention report saved successfully!")
        return redirect("creat_prevention")
    context = {
        
    }
    return render(request, "moh_pages/officers/creat_prevention.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers', 'moh_head'])
def moh_officers_view_prevention(request):
    action = request.GET.get("action")
    prevention = Prevention.objects.all()

    year = request.GET.get('year')
    county = request.GET.get('county')

    # Filter by year
    if year:
        prevention = prevention.filter(date__year=year)

    # Filter by county
    if county:
        prevention = prevention.filter(county__iexact=county)

    context = {
        "action": action,
        "prevention": prevention,
        "selected_year": year,
        "selected_county": county
    }
    return render(request, "moh_pages/officers/view_prevention.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers', 'moh_head'])
def moh_officers_view_prevention_detail(request, id):
    prevention = get_object_or_404(Prevention, id=id)

    context = {
        "prevention": prevention
    }
    return render(request, "moh_pages/officers/prevention_detail.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers'])
def moh_officers_creat_treatment_facility(request):
    if request.method == "POST":

        try:
            d = request.POST

            # BASIC VALIDATION (IMPORTANT)
            if not d.get("county"):
                messages.error(request, "County is required.")
                return redirect("creat_treatment_facility")

            TreatmentFacility.objects.create(

                facility_name=d.get("facility_name"),
                facility_code=d.get("facility_code"),
                facility_type=d.get("facility_type"),
                ownership_type=d.get("ownership_type"),

                county=d.get("county"),
                district=d.get("district"),
                city_town=d.get("city_town"),
                physical_address=d.get("physical_address"),

                contact_person=d.get("contact_person"),
                phone_number=d.get("phone_number"),
                alternate_phone=d.get("alternate_phone"),
                email=d.get("email"),
                website=d.get("website"),

                licensed=(d.get("licensed") == "True"),
                license_number=d.get("license_number"),
                license_issue_date=d.get("license_issue_date") or None,
                license_expiry_date=d.get("license_expiry_date") or None,

                total_beds=d.get("total_beds") or 0,
                male_beds=d.get("male_beds") or 0,
                female_beds=d.get("female_beds") or 0,
                adolescent_beds=d.get("adolescent_beds") or 0,
                current_occupancy=d.get("current_occupancy") or 0,

                detoxification_services=bool(d.get("detoxification_services")),
                inpatient_services=bool(d.get("inpatient_services")),
                outpatient_services=bool(d.get("outpatient_services")),
                counseling_services=bool(d.get("counseling_services")),
                family_therapy=bool(d.get("family_therapy")),
                group_therapy=bool(d.get("group_therapy")),
                medication_assisted_treatment=bool(d.get("medication_assisted_treatment")),
                mental_health_services=bool(d.get("mental_health_services")),
                vocational_training=bool(d.get("vocational_training")),
                aftercare_services=bool(d.get("aftercare_services")),

                medical_doctors=d.get("medical_doctors") or 0,
                psychiatrists=d.get("psychiatrists") or 0,
                psychologists=d.get("psychologists") or 0,
                nurses=d.get("nurses") or 0,
                counselors=d.get("counselors") or 0,
                social_workers=d.get("social_workers") or 0,
                peer_support_workers=d.get("peer_support_workers") or 0,

                operational_status=d.get("operational_status"),
                opening_hours=d.get("opening_hours"),
                accepts_referrals=(d.get("accepts_referrals") == "True"),
                emergency_services_available=(d.get("emergency_services_available") == "True"),

                reporting_year=d.get("reporting_year"),
                reporting_quarter=d.get("reporting_quarter"),
                remarks=d.get("remarks"),
            )

            messages.success(request, "Treatment Facility Saved Successfully ✅")
            return redirect("creat_treatment_facility")

        except Exception as e:
            messages.error(request, f"Error saving facility: {str(e)}")
            return redirect("creat_treatment_facility")

    context = {
    }
    return render(request, "moh_pages/officers/creat_treatment_facility.html", context)

@login_required(login_url='dologin')
@allowed_roles(['moh_officers', 'moh_head'])
def moh_officers_view_treatment_facility(request):
    action = request.GET.get("action")
    
    year = request.GET.get("year")
    county = request.GET.get("county")

    treatment_facility = TreatmentFacility.objects.all().order_by("-created_at")

    # Filter by year
    if year:
        treatment_facility = treatment_facility.filter(created_at__year=year)

    # Filter by county
    if county:
        treatment_facility = treatment_facility.filter(county__iexact=county)

    context = {
        "action": action,
        "year": year,
        "county": county,
        "action": action,
        "treatment_facility": treatment_facility,
    }
    return render(request, "moh_pages/officers/view_treatment_facility.html", context)

