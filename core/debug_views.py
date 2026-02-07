from django.http import JsonResponse
from django.contrib.auth import authenticate
from core.models import User

def debug_auth(request):
    """Debug endpoint to check authentication without exposing sensitive data"""
    
    # Check if root user exists
    try:
        root_user = User.objects.filter(username='root').first()
        user_exists = root_user is not None
        
        if root_user:
            user_info = {
                'exists': True,
                'is_active': root_user.is_active,
                'is_staff': root_user.is_staff,
                'is_superuser': root_user.is_superuser,
            }
            
            # Test password without exposing it
            auth_user = authenticate(username='root', password='root')
            user_info['password_works'] = auth_user is not None
        else:
            user_info = {'exists': False}
            
        return JsonResponse({
            'status': 'ok',
            'user': user_info,
            'total_users': User.objects.count()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
