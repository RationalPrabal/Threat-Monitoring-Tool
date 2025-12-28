import django_filters
from .models import Alert

class AlertFilter(django_filters.FilterSet):
    severity = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.CharFilter(lookup_expr='iexact')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    assigned_to = django_filters.NumberFilter(field_name='assigned_to__id')

    class Meta:
        model = Alert
        fields = ['severity', 'status']
