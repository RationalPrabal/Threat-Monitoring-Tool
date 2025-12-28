from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class SecurityEvent(models.Model):
    class EventType(models.TextChoices):
        INTRUSION = 'intrusion', _('Intrusion Attempt')
        MALWARE = 'malware', _('Malware Detected')
        ANOMALY = 'anomaly', _('Behavioral Anomaly')
        POLICY_VIOLATION = 'policy_violation', _('Policy Violation')
        OTHER = 'other', _('Other')

    class Severity(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical')

    source_name = models.CharField(max_length=255, help_text="e.g. FireWall, IDS, User")
    event_type = models.CharField(max_length=50, choices=EventType.choices)
    severity = models.CharField(max_length=20, choices=Severity.choices)
    description = models.TextField()
    
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    destination_ip = models.GenericIPAddressField(null=True, blank=True)
    
    user_involved = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='events_involved'
    )
    
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_acknowledged = models.BooleanField(default=False)
    raw_data = models.JSONField(default=dict, blank=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events'
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['severity', 'timestamp', 'event_type']),
        ]
        verbose_name = _("Security Event")
        verbose_name_plural = _("Security Events")

    def __str__(self):
        return f"{self.source_name} - {self.event_type} ({self.severity})"

    def is_critical(self):
        return self.severity == self.Severity.CRITICAL

    def is_high_severity(self):
        return self.severity in [self.Severity.HIGH, self.Severity.CRITICAL]

    def should_trigger_alert(self):
        return self.is_high_severity()
