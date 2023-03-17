from django.contrib import messages
from django.contrib import admin

# Register your models here.
from railapp.models import *


@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    list_display = ['username', 'get_role', 'is_staff', 'is_active']
    list_display_links = list_display
    search_fields = list_display

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['role'].label = 'Роль'
        return form

    def get_role(self, obj):
        result = Roles.objects.filter(id=obj.role_id).first()
        return result

    get_role.short_description = 'Роль'

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
    list_display = ['get_name', 'get_start_date', 'get_end_date']
    list_display_links = list_display
    search_fields = ['name']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['name'].label = 'Название станции'
        form.base_fields['start_date'].label = 'Дата прибытия'
        form.base_fields['end_date'].label = 'Дата отправки'
        return form

    def get_name(self, obj):
        return obj.name

    def get_start_date(self, obj):
        return obj.start_date

    def get_end_date(self, obj):
        return obj.end_date

    get_name.short_description = 'Название'
    get_start_date.short_description = 'Дата прибытия'
    get_end_date.short_description = 'Дата отправки'

    def save_model(self, request, obj, form, change):
        if obj.start_date > obj.end_date:
            self.message_user(request, 'Дата прибытия не может быть больше даты отправки!', messages.ERROR)
            return

        obj.save()

@admin.register(StationList)
class AdminStationList(admin.ModelAdmin):
    list_display = ['list_id', 'station']
    list_display_links = list_display
    search_fields = list_display

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