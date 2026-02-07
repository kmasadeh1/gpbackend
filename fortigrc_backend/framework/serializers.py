from rest_framework import serializers
from .models import Domain, SubDomain, Control

class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ['id', 'code', 'title', 'description', 'maturity_level']

class SubDomainSerializer(serializers.ModelSerializer):
    controls = ControlSerializer(many=True, read_only=True)
    
    class Meta:
        model = SubDomain
        fields = ['id', 'name', 'code', 'controls']

class DomainSerializer(serializers.ModelSerializer):
    sub_domains = SubDomainSerializer(many=True, read_only=True)

    class Meta:
        model = Domain
        fields = ['id', 'name', 'code', 'description', 'sub_domains']
