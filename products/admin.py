from django.contrib import admin
from django.db.models import F
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Manufacturer, Product, Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс Продукта в админ панели"""

    # количество товара для быстрого добавления
    PIECES_TO_ADD = 10

    list_display = ('name', 'type', 'manufacturer', 'code', 'is_available',
                    'quantity', 'qty_updated_at', 'price', 'updated_at', 'actions_qty')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_qty/<int:pk>/', self.add_qty, name='add_qty'),
        ]
        return my_urls + urls

    def add_qty(self, request, pk):
        """Метод реализации быстрого добавления количества товара"""
        if request.user.is_staff:
            product = Product.objects.get(pk=pk)
            product.quantity = F('quantity') + self.PIECES_TO_ADD
            product.save()
            product_meta = product._meta
            model_name = product_meta.model_name
            app_name = product_meta.app_label
            return redirect(f'admin:{app_name}_{model_name}_changelist')
        else:
            return HttpResponseForbidden()

    def actions_qty(self, obj):
        """Метод для отображения кнопки быстрого добавления товара"""
        return format_html(
            f'<a class="button" href="{{}}">Добавить {self.PIECES_TO_ADD} шт.</a>&nbsp;',
            reverse('admin:add_qty', args=[obj.pk]),
        )

    actions_qty.short_description = 'ДЕЙСТВИЯ'

