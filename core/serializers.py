from rest_framework import serializers
from .models import Agent, AgentLog, AgentMetric, Waitlist

class AgentSerializer(serializers.ModelSerializer):
    """Full agent serializer with all fields"""
    class Meta:
        model = Agent
        fields = [
            'id', 'name', 'status', 'model', 
            'tasks_completed', 'tasks_failed', 'total_cost',
            'uptime_seconds', 'security_score', 'last_security_check',
            'created_at', 'last_active_at', 'metadata'
        ]
        read_only_fields = ['id', 'created_at']

class AgentSummarySerializer(serializers.ModelSerializer):
    """Lightweight agent serializer for lists"""
    class Meta:
        model = Agent
        fields = ['id', 'name', 'status', 'security_score', 'last_active_at']

class AgentLogSerializer(serializers.ModelSerializer):
    """Agent activity log serializer"""
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    
    class Meta:
        model = AgentLog
        fields = ['id', 'agent', 'agent_name', 'timestamp', 'action', 'target', 'status', 'metadata']
        read_only_fields = ['id', 'timestamp']

class AgentMetricSerializer(serializers.ModelSerializer):
    """Agent metrics serializer"""
    class Meta:
        model = AgentMetric
        fields = ['id', 'agent', 'timestamp', 'tokens_used', 'cost', 'files_accessed', 'tool_calls', 'metadata']
        read_only_fields = ['id', 'timestamp']

class DashboardStatsSerializer(serializers.Serializer):
    """Dashboard summary statistics"""
    total_agents = serializers.IntegerField()
    active_agents = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_security_score = serializers.FloatField()
    recent_alerts = serializers.IntegerField()
