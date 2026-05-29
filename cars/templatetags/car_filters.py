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
        return range(round(float(rating)))
    except (ValueError, TypeError):
        return range(0)
    
@register.simple_tag(takes_context=True)
def active_url(context, url_name):
    """
    Return 'active' if current page URL name matches url_name, else ''.
    Usage: <a class="nav-link {% active_url 'home' %}">
    Requires 'django.template.context_processors.request' in TEMPLATES.
    """
    request = context.get('request')
    if request and request.resolver_match:
        return 'active' if request.resolver_match.url_name == url_name else ''
    return ''
