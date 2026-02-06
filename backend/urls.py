"""
URL configuration for Agent Control Panel backend.
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.react_views import ReactAppView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/waitlist', views.waitlist_signup, name='waitlist-signup'),
    path('api/waitlist/count', views.waitlist_count, name='waitlist-count'),
    path('api/admin/waitlist', views.admin_waitlist, name='admin-waitlist'),
    
    # Catch-all: serve React app for all other routes
    # React Router will handle client-side routing
    re_path(r'^.*$', ReactAppView.as_view(), name='react-app'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
