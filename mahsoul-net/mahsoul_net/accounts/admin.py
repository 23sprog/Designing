from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tickets, Feedbacks

UserAdmin.list_display += ("is_seller", 'is_near_seller',)

UserAdmin.fieldsets[2][1]["fields"] = ("is_active",
                                        "is_staff",
                                        "is_superuser",
                                        'is_seller',
                                        'is_near_seller',
                                        "groups",
                                        "user_permissions",
)



admin.site.register(User, UserAdmin)

@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ("requested_user", "responced_admin", "status", "admin_text_message", "user_text_message",)
    search_fields = ("requested_user", "responced_admin", "status", "admin_text_message", "user_text_message",)
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("requested_user", "responced_admin", "status", "admin_text_message", "user_text_message",)}),
    )


@admin.register(Feedbacks)
class FeedbacksAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("name", "description")}),
    )