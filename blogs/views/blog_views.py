from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from blogs.models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blogs/blog_list.html"
    context_object_name = "posts"
    paginate_by = 12
    
    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(is_published=True)
            .select_related("category", "author")
            .prefetch_related("tags")
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["featured_post"] = (
            BlogPost.objects
            .filter(is_published=True)
            .select_related("category", "author")
            .prefetch_related("tags")
            .first()
        )
        return context
        
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blogs/blog_detail.html"
    context_object_name = "post"
    
    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(is_published=True)
            .select_related("author", "category")
            .prefetch_related("tags", "sections")
        )