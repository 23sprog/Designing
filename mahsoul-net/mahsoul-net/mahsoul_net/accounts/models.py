from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_seller = models.BooleanField(default=False, verbose_name="فروشنده")
    is_near_seller = models.BooleanField(default=False, verbose_name="آماده برای فروشندگی")


class Tickets(models.Model):
    status_items = (
        ("a", "پذیرفته شده"),
        ("i", "در حال بررسی"),
        ("r", "رد شده")
    )
    requested_user = models.OneToOneField(User, on_delete=models.CASCADE,
                                          related_name="ticket", verbose_name="کاربر درخواست داده شده")
    responced_admin = models.ForeignKey(User, on_delete=models.CASCADE,
                                        related_name="tickets", null=True, blank=True, verbose_name="ادمین پاسخگو")
    status = models.CharField(choices=status_items, default="i", max_length=1, verbose_name="وضعیت تیکت")
    admin_text_message = models.TextField(blank=True, null=True, verbose_name="متن مدیر سایت")
    user_text_message = models.TextField(blank=True, null=True, verbose_name="متن کاربر")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "تیکت ها"
        verbose_name = "تیکت"
        ordering = ("created_at",)


    def __str__(self):
        return self.requested_user.username


class Feedbacks(models.Model):
    name = models.CharField(max_length=40, verbose_name="نام")
    description = models.TextField(verbose_name="متن بازخورد")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "بازخورد ها"
        verbose_name = "بازخورد"
        ordering = ("created_at",)

    def __str__(self):
        return self.name