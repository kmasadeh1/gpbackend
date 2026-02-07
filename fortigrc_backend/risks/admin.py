from django.contrib import admin
from .models import Asset, Risk

class RiskInline(admin.TabularInline):
    model = Risk
    extra = 1
    readonly_fields = ('risk_score',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'value')
    list_filter = ('value', 'owner')
    inlines = [RiskInline]

@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('threat', 'asset', 'likelihood', 'impact', 'risk_score', 'status')
    list_filter = ('status', 'likelihood', 'impact')
    readonly_fields = ('risk_score',)
