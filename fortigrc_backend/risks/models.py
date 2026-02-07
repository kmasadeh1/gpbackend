from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Asset(models.Model):
    class Value(models.TextChoices):
        LOW = "LOW", _("Low")
        MEDIUM = "MEDIUM", _("Medium")
        HIGH = "HIGH", _("High")

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assets')
    value = models.CharField(max_length=10, choices=Value.choices, default=Value.MEDIUM)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Risk(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", _("Open")
        MITIGATED = "MITIGATED", _("Mitigated")
        ACCEPTED = "ACCEPTED", _("Accepted")

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='risks')
    threat = models.CharField(max_length=255)
    vulnerability = models.CharField(max_length=255)
    
    likelihood = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    impact = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    
    risk_score = models.PositiveIntegerField(default=0, editable=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.risk_score = self.likelihood * self.impact
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.threat} - {self.risk_score}"
