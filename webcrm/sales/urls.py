from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_sales_views, name='home_sales'),
    path('create-customer/', views.create_customer_view, name='create_customer'),
    path('create-sales-order/', views.create_sales_order_view, name='create_sale'),
]
