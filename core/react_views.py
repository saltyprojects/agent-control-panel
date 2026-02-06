from django.views import View
from django.http import HttpResponse
from django.conf import settings
import os

class ReactAppView(View):
    """
    Serve React app index.html for client-side routing.
    React Router will handle the actual routing.
    """
    def get(self, request, *args, **kwargs):
        # Path to React build index.html
        react_index = os.path.join(settings.BASE_DIR, 'frontend', 'dist', 'index.html')
        
        # Check if React build exists
        if os.path.exists(react_index):
            with open(react_index, 'r') as f:
                return HttpResponse(f.read(), content_type='text/html')
        
        # Fallback error
        return HttpResponse('<h1>React app not built</h1><p>Run: cd frontend && npm run build</p>', status=500)
