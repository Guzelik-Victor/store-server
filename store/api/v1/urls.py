from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import ProductRetrieveListApiView, BasketsViewSet


v1_router = DefaultRouter()
v1_router.register(
    'products',
    ProductRetrieveListApiView,
    basename='Products'
)
v1_router.register(
    'baskets',
    BasketsViewSet,
)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('token-auth/', obtain_auth_token),
]
