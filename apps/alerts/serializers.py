from rest_framework import serializers
from .models import Alert
from apps.events.serializers import EventListSerializer
from apps.accounts.serializers import UserDetailSerializer

class AlertListSerializer(serializers.ModelSerializer):
    event = EventListSerializer(read_only=True)
    assigned_to_user = UserDetailSerializer(source='assigned_to', read_only=True)
    
    class Meta:
        model = Alert
        fields = (
            'id', 'title', 'severity', 'status', 'created_at', 
            'event', 'assigned_to_user', 'tags'
        )

class AlertDetailSerializer(serializers.ModelSerializer):
    event = EventListSerializer(read_only=True)
    assigned_to_user = UserDetailSerializer(source='assigned_to', read_only=True)
    acknowledged_by_user = UserDetailSerializer(source='acknowledged_by', read_only=True)
    resolved_by_user = UserDetailSerializer(source='resolved_by', read_only=True)
    
    class Meta:
        model = Alert
        fields = '__all__'

class AlertUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('status', 'assigned_to', 'resolution_notes', 'tags')
        
    def validate(self, attrs):
        # Add workflow validation logic here if needed
        # e.g. cannot resolve without notes
        if attrs.get('status') == Alert.Status.RESOLVED and not attrs.get('resolution_notes'):
            # Check instance if partial update
            if self.instance and not self.instance.resolution_notes:
                 raise serializers.ValidationError({"resolution_notes": "Required when resolving."})
        return attrs
