from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # api
    path('electronics/', include('products.api.urls')),
]
