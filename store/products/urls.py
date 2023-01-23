from django.urls import path

from .views import ProductsListView, ProductDetailView, basket_add, basket_update, basket_remove

app_name = 'products'


urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path(
        'category/<int:category_id>/',
        ProductsListView.as_view(),
        name='category'
    ),
    path(
        'baskets/add/<int:product_id>/',
        basket_add,
        name='basket_add'
    ),
    path(
        'baskets/update/<int:product_id>/',
        basket_update,
        name='basket_update'
    ),
    path(
        'baskets/remove/<int:basket_id>/',
        basket_remove,
        name='basket_remove'
    ),
]
