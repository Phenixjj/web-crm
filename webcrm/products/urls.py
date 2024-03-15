from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

# Define the URL patterns for the products app.
# Each URL is associated with a view function in the views module.
# The name parameter is used to create URL reversing, which allows you to create URLs dynamically using the {% url %} template tag.
urlpatterns = [
    # The home page of the products app. Lists all products.
    path("", views.list_product_view, name="home_product"),
    # The page for creating a new product.
    path("create/", views.create, name="create"),
    # The detail page for a specific product. The product is identified by its handle.
    path("update/<str:handle>/", views.product_detail_view, name="product_detail"),
]

# If the DEBUG setting is True (i.e. in development), then static files are served from MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
