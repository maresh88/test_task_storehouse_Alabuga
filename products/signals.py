from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Product


@receiver(pre_save, sender=Product)
def update_time_on_qty_update(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        current = instance
        prev = Product.objects.get(id=instance.id)
        if current.quantity != prev.quantity:
            current.qty_updated_at = timezone.now()