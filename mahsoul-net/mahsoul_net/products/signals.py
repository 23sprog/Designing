from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from .models import Products, Shops
from django.utils.text import slugify
from accounts.models import User, Tickets


@receiver(pre_save, sender=Products)
def AutoSlug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = get_unique_slug(instance)


@receiver(pre_save, sender=Products)
def deactive_product_depends_shop(sender, instance, *args, **kwargs):
    if not instance.shop.is_active:
        instance.is_active = False

@receiver(pre_delete, sender=Shops)
def deactive_is_seller(sender, instance, *args, **kwargs):
    if instance.seller:
        user = User.objects.get(id=instance.seller.id)
        user.is_seller = False
        user.save()
        user_tickets = Tickets.objects.filter(requested_user=user)
        if user_tickets.exists():
            for ticket in user_tickets:
                ticket.delete()


@receiver(pre_save, sender=Shops)
def deactive_is_active_products(sender, instance, *args, **kwargs):
    if not instance.is_active:
        products = Products.objects.filter(shop__id=instance.id)
        for product in products:
            if product.is_active:
                product.is_active = False
                product.save()


@receiver(pre_save, sender=Shops)
def set_null_normal_users(sender, instance, *args, **kwargs):
    if not instance.seller.is_seller and not instance.seller.is_superuser:
        instance.seller = None



def get_unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name+"-"+instance.shop.name, allow_unicode=True)

    instance_class = instance.__class__
    queryset = instance_class.objects.filter(slug=slug)

    if queryset.exists():
        new_slug = f"{slug}-{queryset.first().id}"
        return get_unique_slug(instance, new_slug)
    return slug

