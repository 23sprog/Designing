from django import forms
from .models import Products, Shops, Cities
from accounts.models import User
from django.core.exceptions import ValidationError


class CreateProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateProductForm, self).__init__(*args, **kwargs)
        self.fields["shop"].required = False

    class Meta:
        model = Products
        fields = ["name",  "price", "img", "category", "description", "has_weight", "is_active", "shop"]
        widgets = {
            "name": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-name"})
            # "slug": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-slug"})
            , "price": forms.NumberInput({"class": "textbox-based textbox-price create-text-large", "id": "create-price"})
            , "img": forms.FileInput({"id": "image-product", "accept": "image/png, image/gif, image/jpeg"})
            , "category": forms.Select({"class": "textbox-based create-text-normal"})
            , "shop": forms.Select({"class": "textbox-based create-text-large"})
            , "description": forms.Textarea({"id": "description-product"})
            , "has_weight": forms.CheckboxInput({"class": "checkbox-based", "id": "has-weight-product"})
            , "is_active": forms.CheckboxInput({"class": "checkbox-based", "id": "is-active-product"})


        }

    def save(self):
        product = super(CreateProductForm, self).save(commit=False)
        if self.request.user.is_seller:
            product.shop = self.request.user.shop
        product.save()
        return product
    # def clean_slug(self):
    #     slug = self.cleaned_data.get("slug")
    #     slug_is_in_database = Products.objects.filter(slug=slug).exists()
    #     if slug_is_in_database:
    #         raise ValidationError("این اسلاگ در سایت وجود دارد لطفا از اسلاگ دیگری استفاده کنید")
    #     return slug



class UpdateProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
    #     self.instance_id = kwargs.pop('instance_id', None)
        super(UpdateProductForm, self).__init__(*args, **kwargs)
        self.fields["shop"].required = False

    class Meta:
        model = Products
        fields = ["name", "price", "img", "category", "description", "has_weight", "is_active", "shop"]
        widgets = {
            "name": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-name"})
            # "slug": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-slug"})
            , "price": forms.NumberInput({"class": "textbox-based textbox-price create-text-large", "id": "create-price"})
            , "img": forms.FileInput({"id": "image-product", "accept": "image/png, image/gif, image/jpeg"})
            , "category": forms.Select({"class": "textbox-based create-text-normal"})
            , "shop": forms.Select({"class": "textbox-based create-text-large"})
            , "description": forms.Textarea({"id": "description-product"})
            , "has_weight": forms.CheckboxInput({"class": "checkbox-based", "id": "has-weight-product"})
            , "is_active": forms.CheckboxInput({"class": "checkbox-based", "id": "is-active-product"})


        }


    def save(self):
        product = super(UpdateProductForm, self).save(commit=False)
        if self.request.user.is_seller:
            product.shop = self.request.user.shop
        product.save()
        return product
    # def clean_slug(self):
    #     slug = self.cleaned_data.get("slug")
    #     slug_is_in_database = Products.objects.filter(slug=slug)
    #     my_product = Products.objects.get(id=self.instance_id)
    #     same_slug = slug == my_product.slug
    #     if slug_is_in_database:
    #         if same_slug:
    #             return slug
    #         raise ValidationError("این اسلاگ در سایت وجود دارد لطفا از اسلاگ دیگری استفاده کنید")
    #     return slug



class AdminCreateShopsForm(forms.ModelForm):

    class Meta:
        model = Shops
        fields = ["name", "seller", "rank_shop", "city", "description", "is_active", "img"]
        widgets = {
            "name": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-name"}),
            "seller": forms.Select({"class": "textbox-based create-text-normal"}),
            "rank_shop": forms.Select({"class": "textbox-based create-text-large", "id": "rank-shop"}),
            "city": forms.SelectMultiple({"class": "shop-city", "id": "city-shop"})
            , "img": forms.FileInput({"id": "image-product", "accept": "image/png, image/gif, image/jpeg"})
            , "is_active": forms.CheckboxInput({"class": "checkbox-based", "id": "is-active-product"})
            , "description": forms.Textarea({"id": "description-product"})
        }

    def clean_seller(self):
        seller = self.cleaned_data.get("seller", None)
        if seller == None:
            raise ValidationError("لطفا یک فروشنده برای فروشگاه مشخص کنید")
        else:
            return seller


class NearSellerCreateShopsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(NearSellerCreateShopsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Shops
        fields = ["name", "city", "description", "is_active", "img"]
        widgets = {
            "name": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-name"}),
            "city": forms.SelectMultiple({"class": "shop-city", "id": "city-shop"})
            , "img": forms.FileInput({"id": "image-product", "accept": "image/png, image/gif, image/jpeg"})
            , "is_active": forms.CheckboxInput({"class": "checkbox-based", "id": "is-active-product"})
            , "description": forms.Textarea({"id": "description-product"})
        }

    # def save(self):
    #     shop = super(NearSellerCreateShopsForm, self).save(commit=False)
    #     if self.request.user.is_near_seller:
    #         user = User.objects.get(id=self.request.user.id)
    #         user.is_near_seller = False
    #         user.is_seller = True
    #         user.save()
    #         shop.seller = user
    #         shop.rank_shop = "d"
    #         cities = self.cleaned_data.get("city", False)
    #         if cities:
    #             for city in cities:
    #                 print(city)
    #                 shop.city.add(city)
    #                 print(city)
    #         shop.save()
    #     return shop

class AdminUpdateShopsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminUpdateShopsForm, self).__init__(*args, **kwargs)
        self.fields["seller"].required = False


    class Meta:
        model = Shops
        fields = ["name", "description", "seller", "rank_shop", "is_active", "img", "city"]
        widgets = {
            "name": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-name"}),
            "seller": forms.Select({"class": "textbox-based create-text-normal"}),
            "rank_shop": forms.Select({"class": "textbox-based create-text-large", "id": "rank-shop"}),
            "city": forms.SelectMultiple({"class": "shop-city", "id": "city-shop"})
            , "img": forms.FileInput({"id": "image-product", "accept": "image/png, image/gif, image/jpeg"})
            , "is_active": forms.CheckboxInput({"class": "checkbox-based", "id": "is-active-product"})
            , "description": forms.Textarea({"id": "description-product"})
        }

    def clean_seller(self):
        seller = self.cleaned_data.get("seller", None)
        if seller==None:
            raise ValidationError("لطفا یک فروشنده برای فروشگاه مشخص کنید")
        else:
            return seller




class SellerUpdateShopsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SellerUpdateShopsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Shops
        fields = ["name", "description", "is_active", "img", "city"]
        widgets = {
            "name": forms.TextInput({"class": "textbox-based create-text-normal", "id": "create-name"}),
            "city": forms.SelectMultiple({"class": "shop-city", "id": "city-shop"})
            , "img": forms.FileInput({"id": "image-product", "accept": "image/png, image/gif, image/jpeg"})
            , "is_active": forms.CheckboxInput({"class": "checkbox-based", "id": "is-active-product"})
            , "description": forms.Textarea({"id": "description-product"})
        }
