from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (Index,
                            SearchView,
                            ProductFilterMainPageView,
                            CollectionView,
                            CollectionDetailView,
                            ContractUsFormView,
                            CityCategoryView,
                            AboutUsView,)



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Index.as_view(), name="index"),
    path("collection/", CollectionView.as_view(), name="collection"),
    path("collection/details/<int:id>/", CollectionDetailView.as_view(), name="collection_details"),
    path("collection/details/<int:id>/page/<int:page>/", CollectionDetailView.as_view(), name="collection_details"),
    path("city/details/<int:id>/page/", CityCategoryView.as_view(), name="city_category"),
    path("city/details/<int:id>/page/<int:page>/", CityCategoryView.as_view(), name="city_category"),
    path("filter_product/", ProductFilterMainPageView.as_view(), name="product_filter_main_page"),
    path("filter_product/page/<int:page>/", ProductFilterMainPageView.as_view(), name="product_filter_main_page"),
    path("<int:page>/", Index.as_view(), name="index"),
    path("search/", SearchView.as_view(), name="search"),
    path("contract_us/", ContractUsFormView.as_view(), name="contract_us"),
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    path("search/page/<int:page>/", SearchView.as_view(), name="search"),
    path("account/", include("accounts.urls", namespace="accounts")),
    path("product/", include("products.urls", namespace="products")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

