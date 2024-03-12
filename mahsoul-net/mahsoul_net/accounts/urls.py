from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('profile/change_password', UserChangePasswordView.as_view(), name="change_password"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('ticket/', TicketUserMainPageView.as_view(), name="ticket"),
    path('ticket/user_form/', TicketUserMessageView.as_view(), name="ticket_user_form"),
    path('ticket/admin_form/<int:id>/', TicketAdminMessageView.as_view(), name="ticket_admin_form"),
    path('ticket/list/', TicketListView.as_view(), name="ticket_list"),
    path('ticket/list/page/<int:page>/', TicketListView.as_view(), name="ticket_list"),
    path('ticket/accept_admin/<int:id>/', TicketAdminAcceptView.as_view(), name="ticket_admin_accept"),
    path('ticket/accept_user/', TicketUserAcceptView.as_view(), name="ticket_user_accept"),
    path('ticket/delete_user/<int:id>/', TicketUserDeleteView.as_view(), name="ticket_user_delete"),
    path('contract_us_list/', ContractUsListView.as_view(), name="contract_us_list"),
    path('contract_us_list/<int:page>/', ContractUsListView.as_view(), name="contract_us_list"),
]