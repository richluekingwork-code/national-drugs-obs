from django.contrib import admin
from .models import*

# Register your models here.
class FamilyMember_TabularInline(admin.TabularInline):
    model = FamilyMember

class FamilyTracingVerification_admin(admin.ModelAdmin):
    inlines = [FamilyMember_TabularInline]

class TracingActionDetail_TabularInline(admin.TabularInline):
    model = TracingActionDetail

class TracingActionTaken_admin(admin.ModelAdmin):
    inlines = [TracingActionDetail_TabularInline]
    
class CaseClosureApproval_TabularInline(admin.TabularInline):
    model = CaseClosureApproval

class CaseClosure_admin(admin.ModelAdmin):
    inlines = [CaseClosureApproval_TabularInline]

admin.site.register(TracingActionTaken, TracingActionTaken_admin)
admin.site.register(FamilyTracingVerification, FamilyTracingVerification_admin)
admin.site.register(CaseClosure, CaseClosure_admin)

admin.site.register(CommunityOutreachReport)
admin.site.register(ChildAdultAssessments)
admin.site.register(BeneficiaryVerification) 
admin.site.register(BeneficiaryHandover)
admin.site.register(FollowUpVisit)