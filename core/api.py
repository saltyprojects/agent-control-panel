"""
Agent Control Panel - REST API Endpoints
Build #17: Full agent CRUD + dashboard stats
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Agent, AgentLog, AgentMetric
from .serializers import (
    AgentSerializer, AgentSummarySerializer,
    AgentLogSerializer, AgentMetricSerializer,
    DashboardStatsSerializer
)


class AgentViewSet(viewsets.ModelViewSet):
    """
    Agent CRUD API
    
    list: GET /api/agents/
    create: POST /api/agents/
    retrieve: GET /api/agents/{id}/
    update: PUT /api/agents/{id}/
    partial_update: PATCH /api/agents/{id}/
    destroy: DELETE /api/agents/{id}/
    """
    serializer_class = AgentSerializer
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated
    
    def get_queryset(self):
        queryset = Agent.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by security score threshold
        min_security = self.request.query_params.get('min_security')
        if min_security:
            queryset = queryset.filter(security_score__gte=int(min_security))
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AgentSummarySerializer
        return AgentSerializer
    
    @action(detail=True, methods=['post'])
    def heartbeat(self, request, pk=None):
        """Record agent heartbeat - updates last_active_at"""
        agent = self.get_object()
        agent.last_active_at = timezone.now()
        agent.status = 'running'
        agent.save(update_fields=['last_active_at', 'status'])
        return Response({'status': 'ok', 'last_active_at': agent.last_active_at})
    
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get recent logs for this agent"""
        agent = self.get_object()
        logs = agent.logs.all()[:50]
        serializer = AgentLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        """Get metrics for this agent"""
        agent = self.get_object()
        
        # Get time range
        hours = int(request.query_params.get('hours', 24))
        since = timezone.now() - timedelta(hours=hours)
        
        metrics = agent.metrics.filter(timestamp__gte=since)
        
        # Aggregate stats
        stats = metrics.aggregate(
            total_tokens=Sum('tokens_used'),
            total_cost=Sum('cost'),
            total_files=Sum('files_accessed'),
            total_tools=Sum('tool_calls')
        )
        
        return Response({
            'agent_id': str(agent.id),
            'period_hours': hours,
            'totals': stats,
            'recent': AgentMetricSerializer(metrics[:20], many=True).data
        })


class AgentLogViewSet(viewsets.ModelViewSet):
    """Agent logs API"""
    queryset = AgentLog.objects.all()
    serializer_class = AgentLogSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = AgentLog.objects.all()
        
        # Filter by agent
        agent_id = self.request.query_params.get('agent')
        if agent_id:
            queryset = queryset.filter(agent_id=agent_id)
        
        # Filter by status
        log_status = self.request.query_params.get('status')
        if log_status:
            queryset = queryset.filter(status=log_status)
        
        # Filter by action type
        action_type = self.request.query_params.get('action')
        if action_type:
            queryset = queryset.filter(action__icontains=action_type)
        
        return queryset[:100]


@api_view(['GET'])
def dashboard_stats(request):
    """
    GET /api/dashboard/stats/
    Returns aggregated dashboard statistics
    """
    now = timezone.now()
    hour_ago = now - timedelta(hours=1)
    
    agents = Agent.objects.all()
    
    stats = {
        'total_agents': agents.count(),
        'active_agents': agents.filter(
            Q(status='running') | Q(last_active_at__gte=hour_ago)
        ).count(),
        'total_cost': float(agents.aggregate(total=Sum('total_cost'))['total'] or 0),
        'avg_security_score': float(agents.aggregate(avg=Avg('security_score'))['avg'] or 100),
        'recent_alerts': AgentLog.objects.filter(
            status='blocked',
            timestamp__gte=hour_ago
        ).count()
    }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
def health_check(request):
    """
    GET /api/health/
    Simple health check for monitoring
    """
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '0.2.0'
    })
