from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_product, name='home_product'),
    path('create/', views.create, name='create'),
]
