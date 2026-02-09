from rest_framework import serializers
from .models import Asset, Risk

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name', 'value', 'description', 'owner']
        read_only_fields = ['owner']

class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        # Include fields as requested, plus timestamps for utility
        fields = ['id', 'asset', 'threat', 'vulnerability', 'likelihood', 'impact', 'risk_score', 'status', 'created_at', 'updated_at']
        read_only_fields = ('risk_score', 'created_at', 'updated_at')
