import logging
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Avg, Min, Max, Q, F

logger = logging.getLogger(__name__)

class AdminDashboardSelector:
    def __init__(self):
        self.now = timezone.now()
        self.seven_day_ago = self.now - timedelta(days=7)
        self.thirty_day_ago = self.now - timedelta(days=30)
        
    def get_kpi_card(self):
        "Querying overall key performance indicators (KPI Cards)"
        from cars.models import Brand, CarModel, CarVariant, Review, CarImage, Comparison
        
        return {
            "total_brands": Brand.objects.filter(is_active=True).count(),
            "total_models": CarModel.objects.count(),
            "total_variants": CarVariant.objects.count(),
            "active_variants": CarVariant.objects.filter(is_active=True).count(),
            "total_reviews": Review.objects.count(),
            "pending_reviews": Review.objects.filter(is_approved=False).count(),
            "total_images": CarImage.objects.count(),
            "total_comparisons": Comparison.objects.count(),
        }
        
    def get_review_stats(self)->dict:
        from cars.models import Review
        
        avg_rating_global = Review.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg'] or 0
        new_reviews_7d = Review.objects.filter(created_at__gte=self.seven_day_ago).count()
        
        rating_dist = []
        for star in range(1,6):
            cnt = Review.objects.filter(rating=star, is_approved=True).count()
            rating_dist.append({"star": star, "count": cnt})
        return {
            "avg_rating_global": avg_rating_global,
            "new_reviews_7d": new_reviews_7d,
            "rating_dist": rating_dist,
        }
    
    def get_fuel_type_data(self):
        from cars.models import CarVariant
        
        fuel_label_maps = dict(CarVariant.FUEL_TYPE_CHOICES)
        fuel_stats = (CarVariant
                      .objects
                      .values('fuel_type')
                      .annotate(count=Count('id'))
                      .order_by('-count'))
        
        labels = [fuel_label_maps.get(f['fuel_type'], f['fuel_type']) for f in fuel_stats]
        data = [f['count'] for f in fuel_stats]
        return json.dumps(labels), json.dumps(data)
    
    def get_body_chart_data(self):
        """Statistics of the number of vehicles by body type"""
        from cars.models import CarVariant
        
        body_stats = ( CarVariant.objects
                      .filter(car_model__body_type__isnull=False)
                      .annotate(body_name = F('car_model__body_type__name'))
                      .values('body_name')
                      .annotate(count=Count('id'))
                      .order_by('-count')[:8]
                    )
        labels = [b['body_name'] for b in body_stats]
        data = [b['count'] for b in body_stats]
        return json.dumps(labels), json.dumps(data)
    
    def get_price_bracket_chart_data(self):
        """Statistics of vehicles distribution according to selling price ranges"""
        from cars.models import CarVariant
        
        brackets =[
            ('Dưới 500tr', Q(price_min__lt=500_000_000)),
            ('500tr-1tỷ', Q(price_min__gte=500_000_000, price_min__lt=1_000_000_000)),
            ('1tỷ-2tỷ', Q(price_min__gte=1_000_000_000, price_min__lt=2_000_000_000)),
            ('Trên 2 tỷ',Q(price_min__gte=2_000_000_000))
        ]
        labels = [b[0] for b in brackets]
        aggregates = {
            f"count_{i}": Count('id', filter=condition) 
            for i, (_, condition) in enumerate(brackets) 
        }
        stats = CarVariant.objects.aggregate(**aggregates)
        data = list(stats.values())
        return json.dumps(labels), json.dumps(data)
    
    def get_price_overview(self):
        """Calculate the highest, lowest, and average floor prices converted to million VND"""
        from cars.models import CarVariant
        
        price_stats = CarVariant.objects.filter(is_active=True).aggregate(
            min_price=Min('price_min'),
            max_price=Max('price_max'),
            avg_min=Avg('price_min'),
        )
        
        def _to_million(val):
            return round(float(val)/1_000_000, 1) if val else 0
        
        return {
            'min': _to_million(price_stats['min_price']),
            'max': _to_million(price_stats['max_price']),
            'avg_min': _to_million(price_stats['avg_min']),
        }
        
    def get_ranking_and_tables(self):
        """Group ranking queries (Top Brand, Top Rated, Most Variant)"""
        from cars.models import CarModel, Brand
        top_brands = (Brand.objects
                      .annotate(
                          variant_count=Count('car_models__variants'),
                          model_count = Count('car_models', distinct=True)
                      )
                      .filter(variant_count__gt=0)
                      .order_by('-variant_count')[:5]
                      )
        top_rated_models = (CarModel.objects
                     .filter(avg_rating__gt=0)
                     .select_related('brand')
                     .order_by('-avg_rating')[:5]
                     )
        most_variant = (CarModel.objects
                        .annotate(variant_count = Count('variants'))
                        .select_related('brand')
                        .order_by('-variant_count')[:5]
                        )
        return {
            'top_brand': top_brands,
            'top_rated_models': top_rated_models,
            'most_variant': most_variant,
        }
        
    def get_data_completeness(self, total_variants:int):
        """Assess the percentage of technical specification completion"""
        from cars.models import CarVariant
        
        if not total_variants:
            return []
        
        missing_engine = CarVariant.objects.filter(engine__isnull=True).count()
        missing_safety = CarVariant.objects.filter(safety__isnull=True).count()
        missing_dimension= CarVariant.objects.filter(dimension__isnull=True).count()
        missing_performance = CarVariant.objects.filter(performance__isnull=True).count()
        missing_image = CarVariant.objects.filter(variant_images__isnull=True).count()
        
        completeness = [
            {'label': 'Có thông số động cơ',  'done': total_variants - missing_engine,     'total': total_variants},
            {'label': 'Có kích thước',         'done': total_variants - missing_dimension,  'total': total_variants},
            {'label': 'Có thông số an toàn',   'done': total_variants - missing_safety,     'total': total_variants},
            {'label': 'có vận hành',           'done': total_variants - missing_performance, 'total': total_variants},
            {'label': 'Có hình ảnh',           'done': total_variants - missing_image,      'total': total_variants},
        ]
        for item in completeness:
            item['pct'] = round(item['done']/item['total']*100)
        return completeness
    
    def get_full_context(self):
        """The main coordinator function to synthesize all the necessary context for the view"""
        kpis = self.get_kpi_card()
        review_stats = self.get_review_stats()
        rankings = self.get_ranking_and_tables()
        price_overview = self.get_price_overview()
        
        fuel_labels, fuel_data = self.get_fuel_type_data()
        body_labels, body_data = self.get_body_chart_data()
        price_labels, price_data = self.get_price_bracket_chart_data()
        
        context = {
            'title': 'Dashboard - CarCompare Admin',
            'now': self.now,
            
            **kpis,
            **review_stats,
            **rankings,
            
            'fuel_chart_labels':     fuel_labels,
            'fuel_chart_data':       fuel_data,
            'body_chart_labels':     body_labels,
            'body_chart_data':       body_data,
            'price_bracket_labels':  price_labels,
            'price_bracket_data':    price_data,
            
            'price_overview':        price_overview,
            'completeness':          self.get_data_completeness(kpis['total_variants']),
        }
        return context
    
    
    
    