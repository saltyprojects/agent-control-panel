from django.views.generic import TemplateView
from django.conf import settings
import os

class ReactAppView(TemplateView):
    """
    Serve React app index.html for client-side routing.
    React Router will handle the actual routing.
    """
    def get_template_names(self):
        # Serve React build index.html
        react_index = os.path.join(settings.BASE_DIR, 'frontend', 'dist', 'index.html')
        
        # If React build exists, use it
        if os.path.exists(react_index):
            return [react_index]
        
        # Fallback to legacy landing page
        return ['landing.html']
