from django.urls import include, path
from rest_framework import routers
from .api import views

router = routers.DefaultRouter()
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('login/', include('rest_framework.urls', namespace='rest_framework'))
]
