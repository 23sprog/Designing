from django.db import models
from accounts.models import User
from datetime import datetime
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name="نام دسته بندی")
    position = models.IntegerField(verbose_name="جایگاه دسته بندی")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"
        ordering = ("created_at",)

    def __str__(self):
        return self.name


class Cities(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name="نام شهر")
    position = models.IntegerField(verbose_name="جایگاه شهر")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "شهر ها"
        verbose_name = "شهر"
        ordering = ("position",)

    def __str__(self):
        return self.name


class ShopsManager(models.Manager):
    def published(self):
        return self.filter(is_active=True)


class Shops(models.Model):
    ranks = (
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
        ("e", "E"),
        ("f", "F"),
        ("o", "Out of range")
    )
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name="نام فروشگاه")
    seller = models.OneToOneField(User, on_delete=models.CASCADE,related_name="shop", null=True, default=None, verbose_name="فروشنده")
    rank_shop = models.CharField(choices=ranks, default="o", max_length=1, verbose_name="جایگاه فروشگاه")
    city = models.ManyToManyField(Cities, related_name="shops", verbose_name="شهر")
    description = models.TextField(default="Desc", verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="نمایش داده شود؟؟")
    img = models.ImageField(upload_to='images_shop/', null=True, verbose_name="تصویر محصول")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "فروشگاه ها"
        verbose_name = "فروشگاه"
        ordering = ("created_at",)

    def __str__(self):
        return self.name

    objects = ShopsManager()


class ProductsManager(models.Manager):
    def published(self):
        return self.filter(is_active=True)


class Products(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام محصول")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    shop = models.ForeignKey(Shops, related_name="products", on_delete=models.CASCADE, null=True, verbose_name="فروشگاه")
    price = models.SmallIntegerField(verbose_name="قیمت محصول")
    img = models.ImageField(upload_to='images/', null=True, verbose_name="تصویر محصول")
    category = models.ForeignKey(Categories,on_delete=models.SET_NULL, null=True, verbose_name="دسته بندی")
    description = models.TextField(default="Desc", verbose_name="توضیحات")
    has_weight = models.BooleanField(verbose_name="وزن ملاک است؟؟")
    weight = models.SmallIntegerField(null=True, blank=True, verbose_name="وزن")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="نمایش داده شود؟؟")


    def get_absolute_url(self):
        return reverse("products:view_product", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"
        ordering = ("created_at",)

    def __str__(self):
        return self.name

    objects = ProductsManager()


class Comments(models.Model):
    text_message =models.TextField(verbose_name="متن نظر")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="کاربر")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="محصول", related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "نظرات"
        verbose_name = "نظر"
        ordering = ("created_at",)

    def get_date(self):
        time = datetime.now()
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        else:
            if self.created_at.month == time.month:
                return str(time.day - self.created_at.day) + " days ago"
            else:
                if self.created_at.year == time.year:
                    return str(time.month - self.created_at.month) + " months ago"
        return self.created_at


    def __str__(self):
        return self.text_message


class ProductsSeller(models.Model):
    status_items = (
        ("b", "درحال خرید"),
        ("s", "خریداری شده")
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="sold_products", null=True, verbose_name="کالا")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="خریدار")
    status = models.CharField(choices=status_items, default="b", max_length=1, verbose_name="وضعیت سفارش")
    count = models.IntegerField(verbose_name="تعداد کالا")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_overall_price(self):
        return self.product.price * self.count

    class Meta:
        verbose_name_plural = "سبد های خرید"
        verbose_name = "سبد خرید"
        ordering = ("created_at",)

    def __str__(self):
        return self.product

