from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from blogs.models import BlogPost, BlogCategory, BlogTag

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
            .prefetch_related("tags", "sections")
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["featured_post"] = (
            BlogPost.objects
            .filter(is_published=True)
            .select_related("category", "author")
            .prefetch_related("tags", "sections")
            .first()
        )
        context["title"] = "Danh sách bài viết"
        return context
    

class CategoryPostListView(ListView):
    model = BlogPost
    template_name = "blogs/blog_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(BlogCategory, slug=self.kwargs['category_slug'])
        return (
            BlogPost.objects
            .filter(is_published=True, category=self.category)
            .select_related("category", "author")
            .prefetch_related("tags", "sections")
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Chuyên mục: {self.category.name}"
        return context
    
    
class TagPostListView(ListView):
    model = BlogPost
    template_name = "blogs/blog_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        self.tag = get_object_or_404(BlogTag, slug=self.kwargs['tag_slug'])
        return (
            BlogPost.objects
            .filter(is_published=True, tags=self.tag)
            .select_related("category", "author")
            .prefetch_related("tags", "sections")
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Thẻ: #{self.tag.name}"
        return context
        
        
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blogs/blog_detail/blog_detail.html"
    context_object_name = "post"
    
    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(is_published=True)
            .select_related("author", "category")
            .prefetch_related("tags", "sections")
        )
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['tags'] = BlogTag.objects.all()[:20]
        context['recent_posts'] = (BlogPost.objects
                                   .filter(is_published=True)
                                   .order_by('-published_at')[:5])
        
        return context