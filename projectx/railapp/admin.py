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
        form.base_fields['number_route'].label = 'Номер табельного'
        form.base_fields['number_wagon'].label = 'Номер вагона'
        return form

    def get_role(self, obj):
        return obj.role

    def get_number_route(self, obj):
        return obj.number_route

    def get_number_wagon(self, obj):
        return obj.number_wagon

    get_role.short_description = 'Роль'
    get_number_route.short_description = 'Номер табельного'
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
    list_display = ['get_list_id', 'get_station', 'get_start_date', 'get_end_date']
    list_display_links = list_display
    search_fields = list_display

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['start_date'].label = 'Дата прибытия'
        form.base_fields['end_date'].label = 'Дата отправки'
        form.base_fields['list_id'].label = '№ Маршрута'
        form.base_fields['station'].label = 'Станция'
        form.base_fields['type'].label = 'Тип рейса'
        return form

    def get_list_id(self, obj):
        return obj.list_id

    def get_station(self, obj):
        return obj.station

    def get_start_date(self, obj):
        return obj.start_date

    def get_end_date(self, obj):
        return obj.end_date


    get_list_id.short_description = '№ Маршрута'
    get_station.short_description = 'Станция'
    get_start_date.short_description = 'Дата прибытия'
    get_end_date.short_description = 'Дата отправки'

@admin.register(ChatList)
class AdminChatList(admin.ModelAdmin):
    list_display = ['get_chat_name', 'get_created_date', 'get_closed_date', 'get_is_readonly']
    list_display_links = list_display
    search_fields = list_display

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['chat_name'].label = 'Название чата'
        form.base_fields['created_date'].label = 'Дата создания'
        form.base_fields['closed_date'].label = 'Дата закрытия'
        form.base_fields['is_readonly'].label = 'Архивированный'

    def get_chat_name(self, obj):
        return obj.chat_name

    def get_created_date(self, obj):
        return obj.created_date

    def get_closed_date(self, obj):
        return obj.closed_date

    def get_is_readonly(self, obj):
        return obj.is_readonly

    get_chat_name.short_description = 'Название чата'
    get_created_date.short_description = 'Дата создания'
    get_closed_date.short_description = 'Дата закрытия'
    get_is_readonly.short_description = 'Архивированный'

@admin.register(Chat)
class AdminChat(admin.ModelAdmin):
    list_display = ['get_chat_id', 'get_user', 'get_text', 'get_date']
    list_display_links = list_display
    search_fields = list_display


    def get_chat_id(self, obj):
        return obj.chat_id

    def get_user(self, obj):
        return obj.user

    def get_text(self, obj):
        return obj.text

    def get_date(self, obj):
        return obj.date

    get_chat_id.short_description = '№ Чата'
    get_user.short_description = 'Пользователь'
    get_text.short_description = 'Текст'
    get_date.short_description = 'Дата сообщения'

@admin.register(Settings)
class AdminSettings(admin.ModelAdmin):
    list_display = ['key', 'value', 'description']
    list_display_links = list_display
    search_fields = list_display