from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer
from apps.rolepermissions.permissions import IsAdmin

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Audit logs are read-only and accessible only by Admins.
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name', 'status']
    search_fields = ['object_repr', 'changes_dict', 'ip_address']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
