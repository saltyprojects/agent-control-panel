from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """Extended user model for future authentication"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.CharField(max_length=50, default='free')
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'users'

class Waitlist(models.Model):
    """Email waitlist signups"""
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, default='landing')
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'waitlist'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email

class Agent(models.Model):
    """AI Agents being monitored"""
    STATUS_CHOICES = [
        ('idle', 'Idle'),
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='idle')
    model = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Enhanced metrics
    tasks_completed = models.IntegerField(default=0)
    tasks_failed = models.IntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    uptime_seconds = models.IntegerField(default=0)
    
    # Security scoring
    security_score = models.IntegerField(default=100)  # 0-100
    last_security_check = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'agents'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.status})"

class AgentLog(models.Model):
    """Agent activity logs"""
    STATUS_CHOICES = [
        ('allowed', 'Allowed'),
        ('blocked', 'Blocked'),
        ('flagged', 'Flagged'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    target = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'agent_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.agent.name}: {self.action} - {self.status}"

class AgentMetric(models.Model):
    """Agent performance metrics"""
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='metrics')
    timestamp = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    files_accessed = models.IntegerField(default=0)
    tool_calls = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'agent_metrics'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.agent.name}: ${self.cost} ({self.tokens_used} tokens)"
