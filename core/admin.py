from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Waitlist, Agent, AgentLog, AgentMetric

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin"""
    list_display = ['email', 'username', 'plan', 'is_staff', 'date_joined']
    list_filter = ['plan', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Agent Control Panel', {'fields': ('plan', 'metadata')}),
    )

@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    """Waitlist management"""
    list_display = ['email', 'source', 'created_at']
    list_filter = ['source', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        # Usually don't add waitlist entries manually
        return True
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    """Agent monitoring"""
    list_display = ['name', 'user', 'status', 'model', 'created_at', 'last_active_at']
    list_filter = ['status', 'model', 'created_at']
    search_fields = ['name', 'user__email']
    readonly_fields = ['id', 'created_at', 'last_active_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'name', 'status', 'model')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_active_at')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AgentLog)
class AgentLogAdmin(admin.ModelAdmin):
    """Agent activity logs"""
    list_display = ['agent', 'action', 'target_short', 'status', 'timestamp']
    list_filter = ['status', 'action', 'timestamp']
    search_fields = ['agent__name', 'action', 'target']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def target_short(self, obj):
        """Truncate target for display"""
        if not obj.target:
            return '-'
        return obj.target[:50] + '...' if len(obj.target) > 50 else obj.target
    target_short.short_description = 'Target'

@admin.register(AgentMetric)
class AgentMetricAdmin(admin.ModelAdmin):
    """Agent metrics and costs"""
    list_display = ['agent', 'tokens_used', 'cost', 'files_accessed', 'tool_calls', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['agent__name']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # Metrics are usually auto-generated
        return request.user.is_superuser

# Customize admin site
admin.site.site_header = 'Agent Control Panel Admin'
admin.site.site_title = 'Agent Control Panel'
admin.site.index_title = 'Dashboard'
