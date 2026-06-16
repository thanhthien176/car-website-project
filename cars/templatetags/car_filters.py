from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='million_vnd')
def million_vnd(value):
    """Convert raw VND (int/Decimal) → "1,100 triệu".
    Usage: {{ variant.price_min|million_vnd }}

    Args:
        value (_type_): _description_
    """
    if not value:
        return "Liên hệ"
    
    try:
        million = Decimal(str(value))/Decimal(1_000_000)
        return f'{million:,.0f} triệu đồng'
    except Exception:
        return str(value)

@register.filter(name='star_range')
def star_range(rating):
    """
    Convert avg_rating Decimal → range(n) for star icon loop.
    Usage: {% for i in car.avg_rating|star_range %}⭐{% endfor %}
    """
    try:
        rating = float(rating)
        
        stars = []
        
        for i in range(1,6):
            if rating >= i:
                stars.append("bi-star-fill")
            elif rating >= i - 0.5:
                stars.append("bi-star-half")
            else:
                stars.append("bi-star")
            
        return stars                
    except (ValueError, TypeError):
        return []
    
@register.simple_tag(takes_context=True)
def active_url(context, name):
    """
    Return 'active' if current page URL name matches url_name, else ''.
    Usage: <a class="nav-link {% active_url 'home' %}">
    Requires 'django.template.context_processors.request' in TEMPLATES.
    """
    request = context.get('request')
    if request and request.resolver_match:
        match = request.resolver_match  
        return 'active' if name in {match.url_name, match.view_name} else ''
    return ''
