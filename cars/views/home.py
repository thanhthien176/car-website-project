from django.views.generic import TemplateView
from cars.services.car_selector import CarSelector

class HomeView(TemplateView):
    """
    Landing page view.
    Delegates all data fetching to CarSelector 
    """
    template_name = 'cars/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selector = CarSelector()
        context['featured_brands'] = selector.get_featured_brands()
        context['lastest_variants'] = selector.get_latest_variants()
        context['top_rated'] = selector.get_top_rated_models()
        return context