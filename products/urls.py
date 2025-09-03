from django.urls import path

from products.views import ImportView, ListProductsView, ProductView

urlpatterns = [
    path("products", ListProductsView.as_view(), name="list_products"),
    path("products/import", ImportView.as_view(), name="import_products"),
    path("products/<int:pk>", ProductView.as_view(), name="product"),
]