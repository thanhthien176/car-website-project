from django.views.generic import TemplateView
from cars.services.car_selector import CarSelector
from cars.utils import annotate_saved

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
        context['lastest_variants'] = annotate_saved(selector.get_latest_variants(), self.request.user)
        context['top_rated'] = selector.get_top_rated_models()
        return context