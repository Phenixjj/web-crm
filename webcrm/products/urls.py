from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.home_product, name='home_product'),
    path('products/create/', views.create, name='create'),
]
