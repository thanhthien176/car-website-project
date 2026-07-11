from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from blogs.models import BrandHistory


class BrandHistoryView(DetailView):
    """
    Routed at cars:brand_history (/brands/<slug:slug>/history/), but the
    model itself lives in blogs — brand history is content, same category
    of thing as BlogPost and CarDescription, just scoped to one Brand.
 
    The URL slug identifies the Brand, not the BrandHistory row itself,
    so get_object() looks up via the brand__slug relation instead of the
    default slug_field lookup on BrandHistory.slug.
    """

    model = BrandHistory
    template_name = "blogs/brand_history.html"
    context_object_name = "history"
    
    def get_queryset(self):
        return (
            BrandHistory.objects
            .select_related("brand")
            .prefetch_related("sections")
        )
        
    def get_object(self, queryset = None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, brand__slug=self.kwargs["slug"])