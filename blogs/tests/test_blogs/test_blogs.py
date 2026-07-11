from django.test import TestCase

from blogs.tests.helpers import (
    make_blog_post, make_blog_category, make_blog_section, make_blog_tag
    )


class BlogPostTest(TestCase):
    def test_slug_auto_generated_from_title(self):
        post = make_blog_post(title="Tin tức xe điện 2026")
        self.assertTrue(post.slug)
        
    def test_get_absolute_url_contains_slug(self):
        post = make_blog_post(title="Bài test")
        self.assertIn(post.slug, post.get_absolute_url())
        
    def test_category_set_null_when_category_deleted(self):
        category = make_blog_category(name="Test Category")
        post = make_blog_post(title="Test blog", category=category,)
        category.delete()
        post.refresh_from_db()
        self.assertIsNone(post.category)
        
    def test_tags_many_to_many_relation(self):
        tag1 = make_blog_tag(name="SUV")
        tag2 = make_blog_tag(name="Electric")
        post = make_blog_post(title="Test blog")
        post.tags.add(tag1, tag2)
        post.refresh_from_db()
        self.assertEqual(post.tags.count(), 2)
        
    def test_sections_ordered_by_order_field(self):
        post = make_blog_post(title="Bài nhiều sections")
        make_blog_section(post=post, order=2, content="Part 2")
        make_blog_section(post=post, order=1, content="Part 1")
        make_blog_section(post=post, order=3, content="Part 3")
        orders = list(post.sections.values_list("order", flat=True))
        self.assertEqual(orders, [1, 2, 3])
        
    def test_published_at_auto_set_when_published(self):
        post = make_blog_post(title="Test Published", is_published=True)
        self.assertIsNotNone(post.published_at)
        
    def test_published_at_left_empty_when_unpublished(self):
        post = make_blog_post(title="Unpublished", is_published=False)
        self.assertIsNone(post.published_at)
        
        