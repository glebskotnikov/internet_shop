from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import ProductListView, ProductDetailView, ContactsTemplateView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, CategoryListView, CategoryProductsListView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('view/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='view_product'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
    path('category/', CategoryListView.as_view(), name='list_category'),
    path('category/<str:category>', CategoryProductsListView.as_view(), name='category_products')
]
