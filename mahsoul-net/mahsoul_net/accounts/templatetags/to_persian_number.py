from django import template
from django.db.models import Q, Count
from datetime import timedelta, datetime
from products.models import Products, Cities
from accounts.forms import FilterProductMainPageForm


register = template.Library()

@register.filter
def to_persian(value):
    persian_nums = ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"]
    overall_numbers = ""
    value = str(value)
    for val in value:
        type_number = int(val)
        new_number = persian_nums[type_number]
        overall_numbers += new_number
    return overall_numbers


@register.filter
def to_persian_price(value):
    to_per = to_persian(value)
    list_nums = [i for i in str(to_per)]
    length = -abs(len(list_nums))
    f = 0
    for j in range(-3, length, -3):
        list_nums.insert(j-f, ",")
        f+=1
    nums = "".join(list_nums)
    return nums

@register.inclusion_tag('index/filter_section.html')
def filter_products():
    return {"filter_product_form": FilterProductMainPageForm()}


@register.inclusion_tag('index/top_3_products.html')
def top_3_snacks():
    last_month = datetime.now() - timedelta(days=30)
    return {
        "title_section": "پرفروش ترین تنقلات",
        "top_3_snacks": Products.objects.filter(category__name="تنقلات", is_active=True).annotate(count=Count("sold_products", filter=Q(sold_products__created_at__gte=last_month))).order_by("-count")[0:3],
    }


@register.inclusion_tag('index/top_3_products.html')
def top_3_sweets():
    last_month = datetime.now() - timedelta(days=30)
    return {
        "title_section": "پرفروش ترین شیرینی ها",
        "top_3_snacks": Products.objects.filter(category__name="شیرینی", is_active=True).annotate(count=Count("sold_products", filter=Q(sold_products__created_at__gte=last_month))).order_by("-count")[0:3],
    }


@register.inclusion_tag('index/top_3_products.html')
def top_3_nuts():
    last_month = datetime.now() - timedelta(days=30)
    return {
        "title_section": "پرفروش ترین خشکبار",
        "top_3_snacks": Products.objects.filter(category__name="خشکبار", is_active=True).annotate(count=Count("sold_products", filter=Q(sold_products__created_at__gte=last_month))).order_by("-count")[0:3],
    }


@register.inclusion_tag('index/city_main_page.html')
def cities_product(product_id):
    product = Products.objects.get(id=product_id)
    return {
        "cities": Cities.objects.filter(shops=product.shop).order_by("-position")[:2],
    }