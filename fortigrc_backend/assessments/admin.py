from django.contrib import admin
from .models import Assessment, Evidence

class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('control', 'auditor', 'status', 'updated_at')
    list_filter = ('status', 'auditor')
    search_fields = ('control__code', 'control__title')
    inlines = [EvidenceInline]

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'description', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('description', 'assessment__control__code')
