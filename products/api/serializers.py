from rest_framework import serializers

from ..models import Manufacturer, Product, Type


class TypeSerializer(serializers.ModelSerializer):
    """Сериализатор модели типа товара"""
    class Meta:
        model = Type
        fields = ('name',)


class ManufacturerSerializer(serializers.ModelSerializer):
    """Сериализатор модели производителя товара"""
    class Meta:
        model = Manufacturer
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор модели товара"""
    manufacturer = ManufacturerSerializer(read_only=True)
    type = TypeSerializer(read_only=True)
    gross_cost = serializers.CharField(source='get_gross_cost')

    class Meta:
        model = Product
        fields = ('name', 'type', 'manufacturer',
                  'code', 'is_available', 'quantity',
                  'qty_updated_at', 'price', 'gross_cost', 'created_at', 'updated_at')


