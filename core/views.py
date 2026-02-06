from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Waitlist
import json

def landing(request):
    """Serve landing page"""
    return render(request, 'landing.html')

def dashboard(request):
    """Serve dashboard"""
    return render(request, 'index.html')

def workflows(request):
    """Serve workflows page"""
    return render(request, 'workflows.html')

def pricing(request):
    """Serve pricing page"""
    return render(request, 'pricing.html')

def integrations(request):
    """Serve integrations page"""
    return render(request, 'integrations.html')

@csrf_exempt
@require_http_methods(["POST"])
def waitlist_signup(request):
    """Add email to waitlist"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email or '@' not in email:
            return JsonResponse({'error': 'Invalid email'}, status=400)
        
        # Create or get existing
        waitlist, created = Waitlist.objects.get_or_create(
            email=email,
            defaults={'source': 'landing'}
        )
        
        count = Waitlist.objects.count()
        
        return JsonResponse({
            'success': True,
            'count': count,
            'created': created
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def waitlist_count(request):
    """Get waitlist count"""
    count = Waitlist.objects.count()
    return JsonResponse({'count': count})

@api_view(['GET'])
def admin_waitlist(request):
    """Get full waitlist for admin"""
    if not request.user.is_authenticated:
        return Response({'error': 'Unauthorized'}, status=401)
    
    waitlist = Waitlist.objects.all()[:100]
    emails = [{
        'email': w.email,
        'created_at': w.created_at.isoformat(),
        'source': w.source
    } for w in waitlist]
    
    return Response({'emails': emails})
