from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('', include('api.car_api.urls')),
    # path('users/', include('api.users.urls'))
]