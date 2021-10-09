from decimal import ROUND_HALF_UP, Decimal

from django.db import models

from .utils import generate_short_uuid, set_context_for_decimal

# коэффициент добавочной стоимости
VAT_RATE = "0.20"

coins = set_context_for_decimal('0.00', ROUND_HALF_UP)


class CreateUpdateTimeManager(models.Model):
    """Абстрактная модель для добавления времени создания и изменения"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        abstract = True


class Type(CreateUpdateTimeManager):
    """Модель типа товара"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Тип изделия')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

    def __str__(self):
        return self.name


class Manufacturer(CreateUpdateTimeManager):
    """Модель производителя товаров"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя производителя')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Product(CreateUpdateTimeManager):
    """Модель товара"""
    name = models.CharField(max_length=255, verbose_name='Название товара')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, related_name='products', verbose_name='Тип')
    code = models.CharField(max_length=8, editable=False, verbose_name='Код товара')
    is_available = models.BooleanField(default=True, verbose_name='Активен')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    qty_updated_at = models.DateTimeField(
        auto_now=False, editable=False, null=True, verbose_name='Дата последнего изменения кол-ва товара'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    manufacturer = models.ForeignKey(
        'Manufacturer', on_delete=models.CASCADE, related_name='products', verbose_name='Произвоидель'
    )

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'

    @property
    def get_gross_cost(self):
        """Цена товара после добавочной стоимости c округлением"""
        gross_cost = self.price + self.price * Decimal(VAT_RATE)
        return gross_cost.quantize(coins)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.qty_updated_at:
            self.qty_updated_at = self.created_at
        if not self.code:
            self.code = generate_short_uuid()
        super().save(*args, **kwargs)
