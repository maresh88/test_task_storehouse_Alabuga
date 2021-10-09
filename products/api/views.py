from django.db.models import F, Sum
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Manufacturer, Product, Type
from .serializers import ProductSerializer


class ProductListAV(generics.ListAPIView):
    """Вывод всех товаров"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductListByTypeAV(generics.ListAPIView):
    """Вывод всех товаров по типу"""
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        self.type = Type.objects.filter(slug=kwargs.get('type')).first()
        if not self.type:
            return Response({'error': f'Тип товара не найден'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(type=self.type)


class ProductListByManufacturerAV(generics.ListAPIView):
    """Вывод всех товаров по производителю"""
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        self.manufacturer = Manufacturer.objects.filter(slug=kwargs.get('manufacturer')).first()
        if not self.manufacturer:
            return Response({'error': f'Производитель не найден'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(manufacturer=self.manufacturer)


class ProductSummaryAV(APIView):
    """Общая сумма всех товаров на складе"""
    def get(self, request, *args, **kwargs):
        result = Product.objects.aggregate(summary=Sum(F('price') * F('quantity')))
        return Response(result)


class ProductSummaryByTypeAV(APIView):
    """Общая сумма всех товаров по типу товара"""
    def get(self, request, *args, **kwargs):
        type = Type.objects.filter(slug=kwargs.get('type')).first()
        if not type:
            return Response({'error': f'Тип товара не найден'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        result = Product.objects.filter(type=type).aggregate(summary=Sum(F('price') * F('quantity')))
        return Response(result)


class ProductSummaryByManufacturerAV(APIView):
    """Общая сумма всех товаров по производителю"""
    def get(self, request, *args, **kwargs):
        manufacturer = Manufacturer.objects.filter(slug=kwargs.get('manufacturer')).first()
        if not manufacturer:
            return Response({'error': f'Производитель не найден'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        result = Product.objects.filter(manufacturer=manufacturer).aggregate(
            summary=Sum(F('price') * F('quantity')))
        return Response(result)
