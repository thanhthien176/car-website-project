from django.urls import path

from blogs.views import BlogPostListView, BlogPostDetailView

app_name = "blogs"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="post_list"),
    path("<slug:slug>/", BlogPostDetailView.as_view(), name="post_detail"),
]