from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from framework.models import Control

class Assessment(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "NOT_STARTED", _("Not Started")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        COMPLIANT = "COMPLIANT", _("Compliant")
        NON_COMPLIANT = "NON_COMPLIANT", _("Non-Compliant")

    control = models.OneToOneField(Control, on_delete=models.CASCADE, related_name='assessment')
    auditor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assessments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Assessment for {self.control.code} - {self.status}"

class Evidence(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='evidence')
    file = models.FileField(upload_to='evidence/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidence for {self.assessment.control.code}: {self.description}"
