"""
URL configuration for Platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from study_product.views import available_products, product_lessons, product_statistics, product_statistics_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('available-products/', available_products, name='available_products'),
    path('product-lessons/<int:product_id>/', product_lessons, name='product_lessons'),
    path('product-statistics/<int:product_id>/', product_statistics, name='product_statistics'),
    path('product-statistics/', product_statistics_list, name='product_statistics_list'),

]
