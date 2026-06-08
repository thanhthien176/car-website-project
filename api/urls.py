from django.urls import path, include

urlpatterns = [
    path('', include('api.cars.urls')),
    # path('users/', include('api.users.urls'))
]