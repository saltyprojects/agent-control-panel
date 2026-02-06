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
        # Try static files directory first (after collectstatic)
        static_index = os.path.join(settings.STATIC_ROOT, 'index.html')
        
        # Try source directory (development)
        source_index = os.path.join(settings.BASE_DIR, 'frontend', 'dist', 'index.html')
        
        # Check which one exists
        index_path = None
        if os.path.exists(static_index):
            index_path = static_index
        elif os.path.exists(source_index):
            index_path = source_index
        
        if index_path:
            with open(index_path, 'r') as f:
                return HttpResponse(f.read(), content_type='text/html')
        
        # Fallback error with debugging info
        return HttpResponse(
            f'<h1>React app not found</h1>'
            f'<p>Checked: {static_index} (exists: {os.path.exists(static_index)})</p>'
            f'<p>Checked: {source_index} (exists: {os.path.exists(source_index)})</p>',
            status=500
        )
