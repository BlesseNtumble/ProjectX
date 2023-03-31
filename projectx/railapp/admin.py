from django.contrib import messages
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from railapp.models import *


@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "role", "number_route", "number_wagon")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['role'].label = 'Роль'
        form.base_fields['number_route'].label = 'Номер рейса'
        form.base_fields['number_wagon'].label = 'Номер вагона'
        return form

    def get_role(self, obj):
        return obj.role

    def get_number_route(self, obj):
        return obj.number_route

    def get_number_wagon(self, obj):
        return obj.number_wagon

    get_role.short_description = 'Роль'
    get_number_route.short_description = 'Номер рейса'
    get_number_wagon.short_description = 'Номер вагона'

@admin.register(Roles)
class AdminRoles(admin.ModelAdmin):
    list_display = ['__str__']
    list_display_links = list_display
    search_fields = list_display

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['name'].label = 'Название роли'
        return form

@admin.register(Stations)
class AdminStations(admin.ModelAdmin):
    list_display = ['get_name']
    list_display_links = list_display
    search_fields = ['name']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['name'].label = 'Название станции'
        return form

    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'Название'

    def save_model(self, request, obj, form, change):
        if obj.start_date > obj.end_date:
            self.message_user(request, 'Дата прибытия не может быть больше даты отправки!', messages.ERROR)
            return

        obj.save()

@admin.register(StationList)
class AdminStationList(admin.ModelAdmin):
    list_display = ['list_id', 'station', 'get_start_date', 'get_end_date']
    list_display_links = list_display
    search_fields = list_display

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['start_date'].label = 'Дата прибытия'
        form.base_fields['end_date'].label = 'Дата отправки'
        return form

    def get_start_date(self, obj):
        return obj.start_date

    def get_end_date(self, obj):
        return obj.end_date

    get_start_date.short_description = 'Дата прибытия'
    get_end_date.short_description = 'Дата отправки'

@admin.register(ChatList)
class AdminChatList(admin.ModelAdmin):
    list_display = ['chat_name', 'created_date', 'closed_date', 'is_readonly']
    list_display_links = list_display
    search_fields = list_display

@admin.register(Chat)
class AdminChat(admin.ModelAdmin):
    list_display = ['chat_id', 'user', 'text', 'date']
    list_display_links = list_display
    search_fields = list_display

@admin.register(Settings)
class AdminSettings(admin.ModelAdmin):
    list_display = ['key', 'value', 'description']
    list_display_links = list_display
    search_fields = list_display