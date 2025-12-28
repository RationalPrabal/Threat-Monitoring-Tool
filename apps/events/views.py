from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import SecurityEvent
from .serializers import (
    EventListSerializer, EventDetailSerializer, 
    EventCreateSerializer, EventUpdateSerializer
)
from .filters import EventFilter
from apps.rolepermissions.permissions import IsAnalyst, IsAdmin, IsAdminOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = SecurityEvent.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['source_name', 'description', 'source_ip']
    ordering_fields = ['timestamp', 'severity']
    ordering = ['-timestamp']

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == 'retrieve':
            return EventDetailSerializer
        elif self.action == 'create':
            return EventCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EventUpdateSerializer
        return EventDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        event = self.get_object()
        event.is_acknowledged = True
        event.save()
        return Response({'status': 'acknowledged'})
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Implementation for bonus stats
        from django.db.models import Count
        severity_stats = SecurityEvent.objects.values('severity').annotate(count=Count('id'))
        return Response(severity_stats)
