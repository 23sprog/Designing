from django.contrib import admin
from .models import *


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    # fields = ["name", "seller", "position", "city", "description", "is_active", "img"]
    list_display = ("name", "position", )
    date_hierarchy = "created_at"
    search_fields = ("name",)
    ordering = ("created_at",)
    fieldsets = (
        (None, {"fields": ("name", "position",)}),
    )


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "description", "price", "has_weight", "weight", "is_active")
    date_hierarchy = "created_at"
    search_fields = ("name",)
    ordering = ("created_at",)
    fieldsets = (
        (None, {"fields": ("name", "shop", "description", "category","img", "price", "has_weight")}),
        ("گزینه های بیشتر", {"classes": ("collapse",), "fields": ("weight", "is_active")})
    )


@admin.register(Shops)
class ShopsAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    search_fields = ("name",)
    ordering = ("created_at",)
    fieldsets = (
        (None, {"fields": ("name", "seller", "city", "description", "img", "rank_shop")}),
        ("گزینه های بیشتر", {"classes": ("collapse",), "fields": ("is_active",)})
    )


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name", "position")
    search_fields = ("name", "position")
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("name", "position")}),
    )

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("text_message", "user", "product")
    search_fields = ("text_message", "user", "product")
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("text_message", "user", "product")}),
    )



@admin.register(ProductsSeller)
class ProductsSellerAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "status", "count",)
    search_fields = ("product", "user", "status", "count",)
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("product", "user", "status", "count",)}),
    )