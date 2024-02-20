# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_sales, name='home_sales'),
    path('create-customer/', views.create_customer_view, name='create_customer'),
    path('create-sales-order/', views.create_sales_order_view, name='create_sale'),
    path('customer-detail/<str:handle>/', views.customer_detail_view, name='customer_detail'),
    path('customer-delete/<str:handle>/', views.customer_delete_view, name='customer_delete'),
    path('order-detail/<str:order_id>/', views.order_detail_view, name='order_detail'),
]
