from blogs.models import BlogPost

class BlogPostSelector:
    
    @classmethod
    def get_feature_posts(cls):
        qs = (BlogPost.objects
            .filter(is_published=True)
            .prefetch_related('sections')
            .order_by('-updated_at')[:8]
        )
        return qs


