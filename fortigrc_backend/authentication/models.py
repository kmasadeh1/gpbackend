from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        MANAGER = "MANAGER", _("Manager")
        AUDITOR = "AUDITOR", _("Auditor")

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.AUDITOR,
    )
    email = models.EmailField(_("email address"), unique=True)

    REQUIRED_FIELDS = ["email", "role"]

    def __str__(self):
        return self.username
