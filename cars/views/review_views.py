
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from cars.models import CarModel
from cars.forms import ReviewForm

class ReviewSubmitView(FormView):
    template_name = 'cars/forms/review_page.html'
    form_class = ReviewForm
    
    def get_car(self):
        """Helper: get CarModel from URL slug, cache into self._car."""
        if not hasattr(self, '_car'):
            self._car = get_object_or_404(
                CarModel, slug=self.kwargs['slug']
            )
        return self._car
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_model'] = self.get_car()
        return context
    
    def form_valid(self, form):
        review = form.save(commit=False)
        review.car = self.get_car()
        review.save()
        
        success_url = reverse('cars:car_detail', kwargs={'slug': review.car.slug})
        
        # HTMX request? Return HTML fragment instead of redirect
        if self.request.headers.get('HX-Request'):
            return HttpResponse(
                '<div class="alert alert-success">'
                'Cảm ơn! Đánh giá của bạn sẽ giúp ích cho nhiều người</div>'
            ) 
        
        return HttpResponseRedirect(success_url)
    
    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            # Return form with errors for HTMX swap
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_invalid(form)
    
    
    