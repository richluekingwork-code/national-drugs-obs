from django.db import models
from accounts.models import CustomUser
from ldea.models import*



# Register your models here.
class CourtUpdate(BaseModel):
    court_case = models.ForeignKey(Cases, on_delete=models.CASCADE, related_name="updates")

    update_date = models.DateField()

    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("in_trial", "In Trial"),
            ("adjourned", "Adjourned"),
            ("completed", "Completed"),
        ]
    )
    next_hearing_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    court = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'moj'})

    def __str__(self):
        return f"{self.status}"
  
class VictimDetails(BaseModel):
    participant = models.OneToOneField(CaseParticipant, on_delete=models.CASCADE, limit_choices_to={'role': 'victim'})
    condition = models.CharField(max_length=255)  
    referred_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'moj'})

    county = models.CharField(max_length=50, null=True, blank=True)
    referred_to_moh = models.BooleanField(default=False)
    referral_date = models.DateField(null=True, blank=True)

    treatment_status = models.CharField(max_length=100,
        choices=[
            ("pending", "Pending"),
            ("in_treatment", "In Treatment"),
            ("recovered", "Recovered"),
        ],
        default="pending"
    )

    facility_name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Victim - {self.participant.person}"
    
 