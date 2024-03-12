from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from .models import User, Tickets
from products.models import Shops

