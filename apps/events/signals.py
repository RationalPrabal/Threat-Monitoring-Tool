# apps/events/signals.py
# (Wait, need to check where to put this. Plan said apps/events/models.py signals? 
# Usually best in separate signals.py or in models.py if small. 
# Plan says: "post_save signal to auto-create Alert if severity is HIGH or CRITICAL")

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SecurityEvent
from apps.alerts.models import Alert

@receiver(post_save, sender=SecurityEvent)
def create_alert_for_high_severity(sender, instance, created, **kwargs):
    if created and instance.should_trigger_alert():
        # Check if alert already exists (unlikely for new event, but safety check)
        if not Alert.objects.filter(event=instance).exists():
            Alert.objects.create(
                event=instance,
                severity=instance.severity,
                title=f"{instance.get_event_type_display()} Detected",
                description=instance.description,
                status=Alert.Status.OPEN
            )
