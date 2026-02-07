"""
URL configuration for Agent Control Panel backend.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from core import views
from core.api import (
    AgentViewSet, AgentLogViewSet, dashboard_stats, health_check,
    simulate_agents, simulate_activity
)
from core.react_views import ReactAppView

# DRF Router for viewsets
router = DefaultRouter()
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'logs', AgentLogViewSet, basename='agentlog')

urlpatterns = [
    # Admin (redirect /admin to /admin/ for proper Django admin routing)
    path('admin', RedirectView.as_view(url='/admin/', permanent=True)),
    path('admin/', admin.site.urls),
    
    # Health check (before API router)
    path('api/health/', health_check, name='health-check'),
    
    # Dashboard stats
    path('api/dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    
    # Simulation endpoints (for demo/testing)
    path('api/simulate/agents/', simulate_agents, name='simulate-agents'),
    path('api/simulate/activity/', simulate_activity, name='simulate-activity'),
    
    # Waitlist endpoints
    path('api/waitlist', views.waitlist_signup, name='waitlist-signup'),
    path('api/waitlist/count', views.waitlist_count, name='waitlist-count'),
    path('api/admin/waitlist', views.admin_waitlist, name='admin-waitlist'),
    
    # DRF Router (agents, logs)
    path('api/', include(router.urls)),
    
    # Catch-all: serve React app for all other routes
    # React Router will handle client-side routing
    re_path(r'^.*$', ReactAppView.as_view(), name='react-app'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
