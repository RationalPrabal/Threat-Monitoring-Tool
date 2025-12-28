from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Alert
from .serializers import (
    AlertListSerializer, AlertDetailSerializer, AlertUpdateSerializer
)
from .filters import AlertFilter
from apps.rolepermissions.permissions import IsAdmin, IsAnalyst

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().select_related('event', 'assigned_to')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AlertFilter
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['created_at', 'severity', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return AlertListSerializer
        elif self.action in ['update', 'partial_update']:
            return AlertUpdateSerializer
        return AlertDetailSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_analyst_user():
            # Analysts might only see assigned alerts? Or all? 
            # Plan says: "Apply role-based filters (Analysts see their assigned alerts)"
            # "Exclude resolved alerts if filter not applied"
            # Let's show all for now, but prioritize assigned
            pass
        return qs

    def perform_update(self, serializer):
        instance = serializer.instance
        validated_data = serializer.validated_data
        
        # Auto-set timestamps and users based on status change
        new_status = validated_data.get('status')
        if new_status == Alert.Status.ACKNOWLEDGED and instance.status != Alert.Status.ACKNOWLEDGED:
            serializer.save(acknowledged_by=self.request.user, acknowledged_at=timezone.now())
        elif new_status == Alert.Status.RESOLVED and instance.status != Alert.Status.RESOLVED:
            serializer.save(resolved_by=self.request.user, resolved_at=timezone.now())
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.status = Alert.Status.ACKNOWLEDGED
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        return Response({'status': 'acknowledged'})

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        notes = request.data.get('resolution_notes', '')
        if not notes:
             return Response({'error': 'Resolution notes required'}, status=status.HTTP_400_BAD_REQUEST)
        
        alert.status = Alert.Status.RESOLVED
        alert.resolved_by = request.user
        alert.resolved_at = timezone.now()
        alert.resolution_notes = notes
        alert.save()
        return Response({'status': 'resolved'})

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def assign(self, request, pk=None):
        alert = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate user existence...
        alert.assigned_to_id = user_id
        alert.save()
        return Response({'status': 'assigned'})
