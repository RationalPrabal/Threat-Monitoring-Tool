from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.events.models import SecurityEvent

class Alert(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        ACKNOWLEDGED = 'ACKNOWLEDGED', _('Acknowledged')
        RESOLVED = 'RESOLVED', _('Resolved')

    event = models.ForeignKey(SecurityEvent, on_delete=models.CASCADE, related_name='alerts')
    # Denormalized severity for easier querying
    severity = models.CharField(max_length=20, choices=SecurityEvent.Severity.choices)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acknowledged_alerts'
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_alerts'
    )
    
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")

    class Meta:
        ordering = ['-created_at', 'status']
        verbose_name = _("Alert")
        verbose_name_plural = _("Alerts")

    def __str__(self):
        return f"[{self.status}] {self.title}"
