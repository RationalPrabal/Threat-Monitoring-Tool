import django_filters
from .models import SecurityEvent

class EventFilter(django_filters.FilterSet):
    severity = django_filters.CharFilter(lookup_expr='iexact')
    event_type = django_filters.CharFilter(lookup_expr='iexact')
    start_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    source_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = SecurityEvent
        fields = ['severity', 'event_type', 'is_acknowledged']
