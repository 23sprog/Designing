from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from .models import *
from django.views.generic import (DetailView, CreateView, View, UpdateView, DeleteView, ListView, TemplateView, FormView)
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .mixins import *
from accounts.mixins import *
from accounts.paginator import paginator_sprog, get_list_to_ten, get_overall_price_of_carts


class ProductDetailView(DetailView):
    template_name = 'products/product_read.html'
    context_object_name = "product"

    def get_object(self):
        slug = self.kwargs.get("slug")
        self.product = get_object_or_404(Products.objects.published(), slug=slug)
        return self.product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"comments": Comments.objects.filter(product=self.product).order_by("created_at"),
                        "list_one_to_ten": get_list_to_ten()
                        })
        return context


class ProductDetailPreview(LoginRequiredMixin, SellerAdminProductSelfMixin, DetailView):
    template_name = 'products/product_read.html'
    context_object_name = "product"

    def setup(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Products, slug=kwargs.get("slug"), is_active=False)
        super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = Cities.objects.filter(shops=self.instance.shop)
        context.update({"comments": Comments.objects.filter(product=self.instance).order_by("created_at"),
                        "cities": cities
                        })
        return context


class ProductCommentView(LoginRequiredMixin, View):

    def post(self, request):
        text_message = request.POST.get("text_message")
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Products, id=product_id)
        Comments.objects.create(user=request.user, text_message=text_message, product=product)
        if product.is_active:
            return redirect("products:view_product", product.slug)
        else:
            return redirect("products:preview_product", product.slug)


class ProductCreateView(LoginRequiredMixin, SellerAdminMixin, CreateView):
    template_name = "products/product_create.html"
    success_url = reverse_lazy("products:list_product")
    form_class = CreateProductForm

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ProductUpdateView(LoginRequiredMixin, SellerAdminProductSelfMixin, UpdateView):
    template_name = "products/product_create.html"
    success_url = reverse_lazy("products:list_product")
    form_class = UpdateProductForm

    def setup(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Products, id=kwargs.get("id"))
        super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.instance

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        # kwargs["instance_id"] = self.kwargs.get("id")
        return kwargs


class ProductDeleteView(LoginRequiredMixin, SellerAdminProductSelfMixin, DeleteView):
    success_url = reverse_lazy("products:list_product")
    template_name = "products/product_delete.html"
    context_object_name = "product"

    def setup(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Products, id=kwargs.get("id"))
        super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.instance


class ProductListView(LoginRequiredMixin, SellerAdminMixin, ListView):
    template_name = "products/product_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.querysets = Products.objects.all()
            return self.querysets
        elif self.request.user.is_seller:
            self.querysets = Products.objects.filter(shop__seller=self.request.user)
            return self.querysets

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.kwargs.get("page")
        pagin = paginator_sprog(self.querysets, page_num, 2)
        context.update({"pagin": pagin})
        return context

class ProductAddToCartView(LoginRequiredMixin, NormalUserMixin, View):
    def post(self, request):
        post_kwargs = request.POST
        ProductsSeller.objects.create(product_id=post_kwargs.get("product_id"),
                                      user=request.user,
                                      count=post_kwargs.get("count"),
                                      status="b")
        return redirect(reverse("products:list_product_cart"))


class ProductCartView(LoginRequiredMixin, NormalUserMixin, ListView):
    template_name = "products/product_cart.html"
    context_object_name = "product_carts"
    def get_queryset(self):
        self.my_queryset = ProductsSeller.objects.filter(user=self.request.user, status="b")
        return self.my_queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"overall_price_carts": get_overall_price_of_carts(self.my_queryset),
                        "has_product_cart": self.my_queryset.exists()
                        })
        return context


class ProductDeleteCartView(LoginRequiredMixin, NormalUserMixin, View):
    def get(self, request, id):
        ProductsSeller.objects.filter(id=id, status="b").delete()
        # product_cart.delete()
        return redirect("products:list_product_cart")


class ProductCartFinalSectionView(LoginRequiredMixin, NormalUserMixin, View):
    def post(self, request):
        product_carts = ProductsSeller.objects.filter(user=request.user, status="b")
        for product_cart in product_carts:
            product_cart.status = "s"
            product_cart.save()
        return redirect("index")


class AdminShopUpdateView(LoginRequiredMixin, SuperUserMixin, UpdateView):
    template_name = "shops/admin_shop_update.html"
    success_url = reverse_lazy("products:view_shop")
    form_class = AdminUpdateShopsForm

    def setup(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shops, id=kwargs.get("id"))
        super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.shop




class SellerShopUpdateView(LoginRequiredMixin, IsSellerShopMixin, UpdateView):
    template_name = "shops/seller_shop_update.html"
    success_url = reverse_lazy("products:view_shop")
    form_class = SellerUpdateShopsForm

    def setup(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shops, id=kwargs.get("id"))
        super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.shop

    def get_form_kwargs(self):
        kwargs = super(SellerShopUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        cd = form.cleaned_data
        cities = cd.get("city", False)
        if cities:
            for city in cities:
                self.shop.city.add(city)
        self.shop.seller = self.request.user
        self.shop.save()
        return super().form_valid(form)


class AdminShopCreateView(LoginRequiredMixin, SuperUserMixin, CreateView):
    template_name = "shops/shop_create_admin.html"
    success_url = reverse_lazy("products:view_shop")
    form_class = AdminCreateShopsForm
    #
    # def form_valid(self, form):
    #     Shops.objects.create(ana)
    #     return super().form_valid(form)


class NearSellerShopCreateView(LoginRequiredMixin, IsNearSellerMixin, FormView):
    template_name = "shops/shop_create_near_user.html"
    success_url = reverse_lazy("products:view_shop")
    form_class = NearSellerCreateShopsForm

    def get_form_kwargs(self):
        kwargs = super(NearSellerShopCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_near_seller:
            user = User.objects.get(id=self.request.user.id)
            user.is_near_seller = False
            user.is_seller = True
            user.save()
            cd = form.cleaned_data
            shop = Shops.objects.create(name=cd.get("name"), is_active=cd.get("is_active"), rank_shop="d",
                                        description=cd.get("description"),
                                        img=cd.get("img"), seller=user)
            cities = cd.get("city", False)
            if cities:
                for city in cities:
                    print(city)
                    shop.city.add(city)
                    print(city)
            shop.save()
        return super().form_valid(form)

class ShopDeleteView(LoginRequiredMixin, SellerAdminShopMixin, DeleteView):
    success_url = reverse_lazy("index")
    template_name = "products/product_delete.html"
    context_object_name = "shop"

    def setup(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shops, id=kwargs.get("id"))
        super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.shop


class ShopPanelView(LoginRequiredMixin, SellerAdminShopPanelMixin, ListView):

    def setup(self, request, *args, **kwargs):
        if request.user.is_seller:
            self.shop = get_list_or_404(Shops, seller=request.user)
        else:
            self.shop = Shops.objects.all()

        super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return self.shop

    def get_template_names(self):
        if self.request.user.is_superuser:
            return ["shops/admin_shop_view.html"]
        else:
            return ["shops/seller_shop_view.html"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            page_num = self.kwargs.get("page")
            obj_shops = paginator_sprog(self.shop, page_num, 1)
        else:
            obj_shops = self.shop
        context.update({"shops": obj_shops})
        return context


class ShopDetailView(DetailView):
    template_name = "shops/shop_detail.html"
    context_object_name = "shop"

    def get_object(self, queryset=None):
        self.shop = get_object_or_404(Shops.objects.filter(id=self.kwargs["id"],is_active=True),)
        return self.shop

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.kwargs.get("page")
        product = Products.objects.published().filter(shop=self.shop)
        obj_shops = paginator_sprog(product, page_num, 1)
        cities = Cities.objects.filter(shops=self.shop)
        context.update({"pagin": obj_shops, "cities": cities})
        return context


