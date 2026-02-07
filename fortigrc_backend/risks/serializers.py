from rest_framework import serializers
from .models import Asset, Risk

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = '__all__'
        read_only_fields = ('risk_score',)
