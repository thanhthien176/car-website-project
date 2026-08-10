from typing import Any

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from core.forms import ContactMeForm

class TermsView(TemplateView):
    template_name = "core/general_terms.html"

class PrivacyView(TemplateView):
    template_name = "core/privacy_policy.html"

class DisclaimerView(TemplateView):
    template_name = "core/disclaimer.html"
    
class AboutView(TemplateView):
    template_name = "core/about.html"
    
class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactMeForm
    success_url = reverse_lazy("core:contact")
    
    def form_valid(self, form: Any) -> HttpResponse:
        form.save()
        
        if self.request.headers.get('HX-Request'):
            return HttpResponse('''
                <div class="text-center py-5">
                    <i class="bi bi-check-circle-fill text-success" style="font-size: 3rem;"></i>
                    <h3 class="mt-3">Cảm ơn bạn đã liên hệ!</h3>
                    <p class="text-muted">Chúng tôi đã nhận được thông tin và sẽ phản hồi bạn trong thời gian sớm nhất.</p>
                </div>            
            ''')
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            # Return form with errors for HTMX swap
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_invalid(form)    
