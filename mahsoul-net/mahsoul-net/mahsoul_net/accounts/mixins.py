from django.shortcuts import redirect
from django.http import Http404


class UserAthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)


class SuperUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")

class IsNearSellerMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_near_seller:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")

class NormalUserTicketSelfMixin:
    def dispatch(self, request, *args, **kwargs):
        if (not request.user.is_superuser and not request.user.is_seller and not request.user.is_near_seller) and (self.ticket.requested_user == request.user) and self.ticket.status == "r":
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Page Not Found")