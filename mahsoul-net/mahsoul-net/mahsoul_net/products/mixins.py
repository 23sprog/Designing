from django.http import Http404


class SellerAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_seller and request.user.shop) or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")


class NearSellerAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_near_seller or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")

class SellerAdminProductSelfMixin:
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_seller and self.instance.shop == request.user.shop and request.user.shop) or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")



class SellerAdminShopPanelMixin:
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_seller and request.user.shop) or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")

class SellerAdminShopMixin:
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_seller and request.user.shop and request.user.shop == self.shop) or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")


class IsSellerShopMixin:
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_seller and request.user.shop and request.user.shop == self.shop):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")

class NormalUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_seller and not request.user.is_near_seller:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")

