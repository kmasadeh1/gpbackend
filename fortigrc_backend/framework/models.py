from django.db import models
from django.utils.translation import gettext_lazy as _

class Domain(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class SubDomain(models.Model):
    domain = models.ForeignKey(Domain, related_name='sub_domains', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('domain', 'code')

    def __str__(self):
        return f"{self.code} - {self.name}"

class Control(models.Model):
    sub_domain = models.ForeignKey(SubDomain, related_name='controls', on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    maturity_level = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('sub_domain', 'code')

    def __str__(self):
        return f"{self.code} - {self.title}"
