from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, create_order
from . import views

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path('', views.home, name='home'),
    path("api/", include(router.urls)),
    path("create/", create_order, name="create_order"),
]
