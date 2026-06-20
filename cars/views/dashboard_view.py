import logging
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from ..services.dashboard import AdminDashboardSelector

logger = logging.getLogger(__name__)

# Create your views here.
@staff_member_required
def admin_dashboard(request):
    context = cache.get('admin_dashboard_context')
    if not context:
        logger.debug("Dashboard cache miss - rebuilding context")
        selector = AdminDashboardSelector()     
        context = selector.get_full_context()
        
        cache.set('admin_dashboard_context', context, 600)
    else:
        logger.debug("Dashboard cache hit")
    
    return render(request, 'admin/cars/dashboard.html', context)
