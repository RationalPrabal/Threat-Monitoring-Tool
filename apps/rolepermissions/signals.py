from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import RolePermission
from apps.accounts.models import User

# This signal could auto-assign permissions or log changes
# For now, we might want to seed initial permissions after migrate
# But post_migrate is tricky. 
# Plan says: "Auto-create RolePermission entries when user role changes" -> Maybe not needed if logic is hardcoded.
# "Log permission changes".

# Step 2.3 says: "PreDefinedRoles fixture with permissions"
