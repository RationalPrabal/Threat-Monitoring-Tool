from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class RolePermission(models.Model):
    role = models.CharField(
        max_length=20,
        choices=User.Role.choices,
        unique=True # One entry per role defining its capabilities? Or many per role?
        # Plan says: "role", "permission" (e.g. 'view_events'). 
        # Usually one mapping per role-permission pair.
    )
    permission = models.CharField(max_length=100, help_text="codename of permission")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name = _('Role Permission')
        verbose_name_plural = _('Role Permissions')

    def __str__(self):
        return f"{self.role} - {self.permission}"
