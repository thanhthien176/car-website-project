from django.views.generic import TemplateView
from cars.services.model_services.car_selector import CarSelector
from blogs.selectors import BlogPostSelector

class HomeView(TemplateView):
    """
    Landing page view.
    Delegates all data fetching to CarSelector 
    """
    template_name = 'cars/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selector = CarSelector()
        blogs = BlogPostSelector.get_feature_posts()
        context['featured_brands'] = selector.get_featured_brands()
        context['top_rated'] = selector.get_top_rated_models()
        context['posts'] = blogs
        return context