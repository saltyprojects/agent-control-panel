"""
URL configuration for Agent Control Panel backend.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Frontend pages
    path('', views.landing, name='landing'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('workflows.html', views.workflows, name='workflows'),
    path('pricing.html', views.pricing, name='pricing'),
    path('integrations.html', views.integrations, name='integrations'),
    
    # API endpoints
    path('api/waitlist', views.waitlist_signup, name='waitlist-signup'),
    path('api/waitlist/count', views.waitlist_count, name='waitlist-count'),
    path('api/admin/waitlist', views.admin_waitlist, name='admin-waitlist'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
