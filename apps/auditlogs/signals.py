from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from .middleware import get_current_user, get_current_request
from apps.events.models import SecurityEvent
from apps.alerts.models import Alert
from apps.accounts.models import User

# List of models to track
TRACKED_MODELS = [SecurityEvent, Alert, User]

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    user = get_current_user()
    if not user or not user.is_authenticated:
        # Try to get from instance if available (e.g. created_by)
        if hasattr(instance, 'created_by') and instance.created_by:
            user = instance.created_by
        else:
            return # Cannot log without user context (or log as system?)

    action = AuditLog.Action.CREATE if created else AuditLog.Action.UPDATE
    
    # Capture changes (simplistic approach)
    changes = {}
    # Real implementation would compare against old state, but post_save only gives new state.
    # For robust diffs, pre_save is needed or a libraries like django-simple-history.
    # Here we just log the current state.
    
    request = get_current_request()
    ip = request.META.get('REMOTE_ADDR') if request else None

    AuditLog.objects.create(
        user=user,
        action=action,
        content_object=instance,
        object_repr=str(instance),
        model_name=sender.__name__,
        changes_dict={'new_state': str(instance)}, # Placeholder for full diff
        ip_address=ip,
        status='SUCCESS'
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    user = get_current_user()
    if not user or not user.is_authenticated:
        return

    request = get_current_request()
    ip = request.META.get('REMOTE_ADDR') if request else None

    AuditLog.objects.create(
        user=user,
        action=AuditLog.Action.DELETE,
        content_object=instance,
        object_repr=str(instance),
        model_name=sender.__name__,
        ip_address=ip,
        status='SUCCESS'
    )
