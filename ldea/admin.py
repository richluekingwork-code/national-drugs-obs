from django.contrib import admin
from .models import*
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(DrugType)
admin.site.register(DrugRaid)
admin.site.register(Person)
admin.site.register(Cases)
admin.site.register(CaseParticipant)
admin.site.register(Seizure)
admin.site.register(Arrest)
admin.site.register(VictimHistory)
admin.site.register(Evidence)
