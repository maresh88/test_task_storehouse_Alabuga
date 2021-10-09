from django.urls import path

from . import views

urlpatterns = [
    # вывод всех товаров
    path('all/', views.ProductListAV.as_view(), name='product-list'),
    # вывод суммы товаров по параметрам
    path('summary/', views.ProductSummaryAV.as_view(), name='product-summary'),
    path('summary/type/<str:type>/', views.ProductSummaryByTypeAV.as_view(), name='product-summary-by-type'),
    path('summary/manufacturer/<str:manufacturer>/', views.ProductSummaryByManufacturerAV.as_view(),
         name='product-summary-by-manufacturer'),
    # вывод товаров по параметрам
    path('type/<str:type>/', views.ProductListByTypeAV.as_view(), name='product-by-type'),
    path('manufacturer/<str:manufacturer>/', views.ProductListByManufacturerAV.as_view(),
         name='product-by-manufacturer'),
]
