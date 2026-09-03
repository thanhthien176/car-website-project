from django.urls import path

from blogs.views import (BlogPostListView, 
                         CategoryPostListView, 
                         TagPostListView, 
                         BlogPostDetailView)

app_name = "blogs"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="post_list"),
    
    path('category/<slug:category_slug>/', CategoryPostListView.as_view(), name='category_post_list'),
    path('tag/<slug:tag_slug>/', TagPostListView.as_view(), name='tag_post_list'),
    
    path("<slug:slug>/", BlogPostDetailView.as_view(), name="post_detail"),
]