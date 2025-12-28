from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Custom user manager for role-based users.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)

    def get_admins(self):
        return self.filter(role='ADMIN')

    def get_analysts(self):
        return self.filter(role='ANALYST')


class User(AbstractUser):
    """
    Custom User model supporting roles.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        ANALYST = 'ANALYST', _('Security Analyst')

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ANALYST,
        help_text=_("User role for permission management")
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.')
    )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Use email or username? Django AbstractUser uses username by default.
    # We keep username but require email.
    
    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'accounts_user'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def is_admin_user(self):
        return self.role == self.Role.ADMIN

    def is_analyst_user(self):
        return self.role == self.Role.ANALYST
