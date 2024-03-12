from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View, ListView, FormView, UpdateView, TemplateView, CreateView
from .forms import *
from .models import User
from django.contrib.auth import login, authenticate, logout
from products.models import Products, ProductsSeller
from django.db.models import Q, Count
from .mixins import *
from .paginator import paginator_sprog
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from products.mixins import NormalUserMixin

class Index(View):
    template_name = "index/index.html"
    query_class = Products.objects.published()
    product_filter_form = FilterProductMainPageForm
    def get(self, request):
        page_num = request.GET.get("page")
        pagin = paginator_sprog(self.query_class, page_num, 1)
        return render(request, "index/index.html", {"pagin": pagin, })


class CollectionView(TemplateView):
    template_name = "index/collection_category.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Categories.objects.all()
        context.update({"categories": categories})
        return context


class CollectionDetailView(ListView):
    template_name = "index/collection_details.html"

    def get_queryset(self):
        self.category_id = self.kwargs.get("id")
        self.querysets = Products.objects.published().filter(category_id=self.category_id)
        return self.querysets

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.kwargs.get("page")
        pagin = paginator_sprog(self.querysets, page_num, 1)
        context.update({"pagin": pagin, "category_id":self.category_id})
        return context


class CityCategoryView(ListView):
    template_name = "index/city_collection.html"

    def get_queryset(self):
        self.city_id = self.kwargs.get("id")
        self.querysets = Products.objects.published().filter(shop__city=self.city_id)
        return self.querysets

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.kwargs.get("page")
        pagin = paginator_sprog(self.querysets, page_num, 1)
        city = Cities.objects.get(id=self.city_id)
        context.update({"pagin": pagin, "city_id": self.city_id, "city": city})
        return context

class SearchView(ListView):
    template_name = "index/search.html"

    def get_queryset(self):
        global search
        search = self.request.GET.get("search")
        self.querysets = Products.objects.published().filter(Q(name__icontains=search) |
                                                   Q(description__icontains=search) | Q(shop__name__icontains=search))
        return self.querysets

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.kwargs.get("page")
        pagin = paginator_sprog(self.querysets, page_num, 1)
        context.update({"search": search, "pagin": pagin})
        return context


class UserRegisterView(UserAthenticatedMixin, View):
    form_class = RegisterForm

    def get(self, request):
        return render(request, "registration_user/register.html", {"form": self.form_class})

    def post(self, request):
        form_check = self.form_class(request.POST)
        if form_check.is_valid():
            cd_form = form_check.cleaned_data
            user = User.objects.create_user(username=cd_form.get("username"),
                                     email=cd_form.get("email"),
                                     password=cd_form.get("password"))
            login(request, user)
            return redirect("index")
        return render(request, "registration_user/register.html", {"form": form_check})


class UserLoginView(UserAthenticatedMixin, FormView):
    form_class = LoginForm
    template_name = "registration_user/login.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form_cd = form.cleaned_data
        user = authenticate(username=form_cd.get("username"), password=form_cd.get("password"))
        login(self.request, user)
        return super().form_valid(form)


class ProductFilterMainPageView(ListView):
    template_name = "index/filter_product.html"

    def get_queryset(self):
        self.cd_get = self.request.GET
        self.query_set_product = Products.objects.published().filter(Q(shop__city__name=self.cd_get.get("city")) |
                                                                     Q(shop__name=self.cd_get.get("shop_name")) |
                                                                     Q(category__name=self.cd_get.get("category")))
        return self.query_set_product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_get = {"shop_city": self.cd_get.get("city"), "category": self.cd_get.get("category"), "shop_id": self.cd_get.get("shop_name")}
        page_num = self.kwargs.get("page")
        pagin = paginator_sprog(self.query_set_product, page_num, 1)
        context.update({"obj_get": obj_get, "pagin": pagin,
                        "filter_product_form": FilterProductMainPageForm()
                        })
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "registration_user/profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.request.user.id)

    def get_form_kwargs(self):
        kwargs = super(UserProfileView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect("index")


class UserChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "registration_user/change_password.html"
    form_class = UserChangePasswordForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        user = User.objects.get(id=self.request.user.id)
        user.set_password(form.cleaned_data.get("new_password"))
        user.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TicketUserMainPageView(LoginRequiredMixin, NormalUserMixin, TemplateView):
    template_name = "tickets/ticket_main_page_user.html"


class TicketUserMessageView(LoginRequiredMixin, NormalUserMixin, FormView):
    template_name = "tickets/ticket_form_user.html"
    success_url = reverse_lazy("accounts:ticket")
    form_class = TicketUserMessageForm

    def form_valid(self, form):
        user_text_message = form.cleaned_data.get("user_text_message")
        Tickets.objects.create(status="i", user_text_message=user_text_message, requested_user=self.request.user)
        return super().form_valid(form)


class TicketListView(LoginRequiredMixin, SuperUserMixin, ListView):
    template_name = "tickets/ticket-list.html"

    def get_queryset(self):
        self.query_set = Tickets.objects.filter(status="i")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.kwargs.get("page")
        pagin = paginator_sprog(self.query_set, page_num, 5)
        context.update({"pagin": pagin})
        return context

class TicketAdminMessageView(LoginRequiredMixin, SuperUserMixin, FormView):
    template_name = "tickets/ticket_form_admin.html"
    success_url = reverse_lazy("accounts:ticket_list")
    form_class = TickeAdminMessageForm

    def form_valid(self, form):
        ticket = Tickets.objects.get(id=self.kwargs.get("id"))
        ticket.status = "r"
        ticket.admin_text_message = form.cleaned_data.get("admin_text_message")
        ticket.responced_admin = self.request.user
        ticket.save()
        return super().form_valid(form)


class TicketAdminAcceptView(LoginRequiredMixin, SuperUserMixin, View):

    def setup(self, request, *args, **kwargs):
        self.ticket = Tickets.objects.get(id=kwargs.get("id"))
        super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return render(request, "tickets/accept_ticket_admin.html", {"ticket": self.ticket})

    def post(self, request, *args, **kwargs):
        self.ticket.responced_admin = request.user
        self.ticket.status = "a"
        requested_user = User.objects.get(id=self.ticket.requested_user.id)
        requested_user.is_near_seller = True
        requested_user.save()
        self.ticket.save()
        return redirect("accounts:ticket_list")

class TicketUserAcceptView(LoginRequiredMixin,IsNearSellerMixin,TemplateView):
    template_name = "tickets/accept_ticket_user.html"


class TicketUserDeleteView(LoginRequiredMixin, NormalUserTicketSelfMixin, View):
    def setup(self, request, *args, **kwargs):
        self.ticket = Tickets.objects.get(id=kwargs.get("id"))
        super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.ticket.delete()
        return redirect("accounts:ticket")




class ContractUsFormView(CreateView):
    template_name = "footer/contact_us.html"
    success_url = reverse_lazy("index")
    form_class = ContractUsForm


class ContractUsListView(LoginRequiredMixin, SuperUserMixin, ListView):
    template_name = "footer/contract_us_detail.html"

    def get_queryset(self):
        self.query_set = Feedbacks.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_num = self.kwargs.get("page")
        pagin = paginator_sprog(self.query_set, page_num, 10)
        context.update({"pagin": pagin})
        return context

class AboutUsView(TemplateView):
    template_name = "footer/about_us.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "city_count":Cities.objects.all().count(),
            "product_count": Products.objects.published().count(),
            "shops_count": Shops.objects.filter(is_active=True).count(),
        })
        return context


