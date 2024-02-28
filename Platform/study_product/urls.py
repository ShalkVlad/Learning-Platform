from django.urls import path
from .views import available_products, product_lessons

urlpatterns = [
    path('available-products/', available_products, name='available_products'),
    path('product-lessons/<int:product_id>/', product_lessons, name='product_lessons'),
]
