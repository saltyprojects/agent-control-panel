"""
Agent Control Panel - REST API Endpoints
Build #19: Real-time agent simulation API
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
import random
import uuid

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


@api_view(['GET'])
def simulate_agents(request):
    """
    GET /api/simulate/agents/?count=5
    Generate simulated agent data for demo/testing
    Returns realistic agent status, metrics, and activity
    """
    count = min(int(request.query_params.get('count', 5)), 20)
    now = timezone.now()
    
    agent_names = [
        "CustomerSupport-AI", "DataAnalyzer-Pro", "CodeReviewer-v2",
        "ContentGenerator", "SecurityScanner", "EmailAssistant",
        "SocialMediaBot", "ResearchAgent", "TaskAutomation",
        "ChatModerator", "DocumentProcessor", "LeadQualifier"
    ]
    
    models = [
        "claude-opus-4-5", "claude-sonnet-4-5", "gpt-4-turbo",
        "gpt-4o", "gemini-pro", "claude-3-opus"
    ]
    
    statuses = ['running', 'idle', 'running', 'running', 'stopped']
    actions = [
        'file_read', 'file_write', 'api_call', 'database_query',
        'email_send', 'slack_post', 'web_scrape', 'data_analysis'
    ]
    
    agents = []
    for i in range(count):
        name = random.choice(agent_names)
        agent_status = random.choice(statuses)
        
        # Simulate activity
        minutes_ago = random.randint(1, 120)
        last_active = now - timedelta(minutes=minutes_ago)
        
        # Simulate costs and tokens
        tokens = random.randint(5000, 500000)
        cost_per_1k = random.uniform(0.002, 0.03)
        total_cost = (tokens / 1000) * cost_per_1k
        
        # Security score (running agents generally higher)
        if agent_status == 'running':
            security_score = random.randint(85, 100)
        else:
            security_score = random.randint(60, 95)
        
        agent_data = {
            'id': str(uuid.uuid4()),
            'name': f"{name}-{i+1}",
            'status': agent_status,
            'model': random.choice(models),
            'last_active_at': last_active.isoformat(),
            'tasks_completed': random.randint(10, 1000),
            'tasks_failed': random.randint(0, 20),
            'total_cost': round(total_cost, 4),
            'security_score': security_score,
            'uptime_seconds': random.randint(3600, 86400),
            'metadata': {
                'tokens_used': tokens,
                'files_accessed': random.randint(5, 200),
                'api_calls': random.randint(10, 500),
                'last_action': random.choice(actions)
            }
        }
        agents.append(agent_data)
    
    # Calculate aggregate stats
    total_cost = sum(a['total_cost'] for a in agents)
    avg_security = sum(a['security_score'] for a in agents) / len(agents)
    active_count = sum(1 for a in agents if a['status'] == 'running')
    
    return Response({
        'count': count,
        'agents': agents,
        'stats': {
            'total_agents': count,
            'active_agents': active_count,
            'total_cost': round(total_cost, 2),
            'avg_security_score': round(avg_security, 1),
            'timestamp': now.isoformat()
        }
    })


@api_view(['GET'])
def simulate_activity(request):
    """
    GET /api/simulate/activity/?limit=20
    Generate simulated agent activity logs
    """
    limit = min(int(request.query_params.get('limit', 20)), 100)
    now = timezone.now()
    
    actions = [
        'file_read', 'file_write', 'file_delete', 'api_call',
        'database_query', 'email_send', 'slack_post', 'web_request',
        'code_execute', 'data_analysis', 'model_call', 'tool_use'
    ]
    
    targets = [
        '/etc/passwd', 'user_data.csv', 'config.json',
        'https://api.stripe.com', 'database://prod',
        'admin@company.com', '#general', 'payment_processor'
    ]
    
    statuses_weights = [
        ('allowed', 70), ('flagged', 20), ('blocked', 10)
    ]
    
    logs = []
    for i in range(limit):
        minutes_ago = random.randint(0, 180)
        timestamp = now - timedelta(minutes=minutes_ago)
        
        # Weighted random status
        status_choice = random.choices(
            [s[0] for s in statuses_weights],
            weights=[s[1] for s in statuses_weights]
        )[0]
        
        action = random.choice(actions)
        target = random.choice(targets)
        
        log_data = {
            'id': str(uuid.uuid4()),
            'timestamp': timestamp.isoformat(),
            'action': action,
            'target': target,
            'status': status_choice,
            'agent_name': f"Agent-{random.randint(1, 10)}",
            'metadata': {
                'duration_ms': random.randint(10, 5000),
                'tokens': random.randint(100, 10000) if 'model' in action else 0
            }
        }
        logs.append(log_data)
    
    # Sort by timestamp desc
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return Response({
        'count': len(logs),
        'logs': logs
    })
