from django.contrib import admin
from .models import Domain, SubDomain, Control

class SubDomainInline(admin.TabularInline):
    model = SubDomain
    extra = 1

class ControlInline(admin.TabularInline):
    model = Control
    extra = 1

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    inlines = [SubDomainInline]

@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'domain')
    list_filter = ('domain',)
    inlines = [ControlInline]

@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'sub_domain', 'maturity_level')
    list_filter = ('sub_domain__domain', 'sub_domain', 'maturity_level')
    search_fields = ('code', 'title', 'description')
