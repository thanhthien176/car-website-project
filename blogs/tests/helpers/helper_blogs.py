from email.policy import default

from cars.tests.helpers import make_variant, make_brand, make_car_model

from blogs.models import (
    BlogPost, BlogCategory, BlogSection, BlogTag,
    CarDescription, CarDescriptionSection,
    BrandHistory, BrandHistorySection,
)

def make_blog_category(name="Tin tức") -> BlogCategory:
    return BlogCategory.objects.get_or_create(
        name=name, defaults={'slug': name.lower()}
    )[0]
    
def make_blog_tag(name="Toyota") -> BlogTag:
    return BlogTag.objects.get_or_create(
        name=name, defaults={'slug': name.lower()}
    )[0]
    
def make_blog_post(**kwargs) -> BlogPost:
    defaults = dict(title="Bài viết mẫu")
    defaults.update(kwargs)
    return BlogPost.objects.create(**defaults)

def make_blog_section(post=None, **kwargs) -> BlogSection:
    if post is None:
        post = make_blog_post()
    defaults = dict(post=post, content="Nội dung mẫu")
    defaults.update(kwargs)
    return BlogSection.objects.create(**defaults)

def make_car_description(car_model=None, variant=None, **kwargs) -> CarDescription:
    """
    variant=None (default) creates a shared, car_model-level description.
    Pass an explicit variant for a variant-specific description.
    """
    if car_model is None:
        car_model = variant.car_model if variant else make_car_model()
    defaults = dict(car_model=car_model, variant=variant, title="Mô tả xe")
    defaults.update(kwargs)
    return CarDescription.objects.create(**defaults)

def make_car_description_section(description=None, **kwargs) -> CarDescriptionSection:
    if description is None:
        description = make_car_description()
    defaults = dict(description=description, content="Nội dung mẫu")
    defaults.update(kwargs)
    return CarDescriptionSection.objects.create(**defaults)

def make_brand_history(brand=None, **kwargs) -> BrandHistory:
    if brand is None:
        brand = make_brand()
    defaults = dict(brand=brand, title=f"Lịch sử thương hiệu {brand.name}")
    defaults.update(kwargs)
    return BrandHistory.objects.create(**defaults)

def make_brand_history_section(history=None, **kwargs) -> BrandHistorySection:
    if history is None:
        history = make_brand_history()
    defaults = dict(history=history, content="Nội dung mẫu")
    defaults.update(kwargs)
    return BrandHistorySection.objects.create(**defaults)
        
        
    

