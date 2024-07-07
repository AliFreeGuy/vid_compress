from django.contrib import admin
from .models import BotModel, PlansModel, SettingModel, UserPlanModel
from django.utils import timezone
from jdatetime import datetime


def is_registered(model):
    """Check if a model is already registered with the admin site."""
    return model in admin.site._registry

if not is_registered(BotModel):
    @admin.register(BotModel)
    class BotModelAdmin(admin.ModelAdmin):
        list_display = ('name', 'username', 'token')
        search_fields = ('name', 'username', 'token')
        list_filter = ('name',)

if not is_registered(PlansModel):
    @admin.register(PlansModel)
    class PlansModelAdmin(admin.ModelAdmin):
        list_display = ('name_fa', 'name_en', 'tag', 'day', 'volume', 'is_active')
        search_fields = ('name_fa', 'name_en', 'tag')
        list_filter = ('is_active', 'day', 'volume')
        list_editable = ('is_active',)

if not is_registered(SettingModel):
    @admin.register(SettingModel)
    class SettingModelAdmin(admin.ModelAdmin):
        list_display = ('bot', 'admin_chat_id', 'video_limit', 'watermark_text', 'channel_url')
        search_fields = ('bot__name', 'admin_chat_id', 'channel_url')
        list_filter = ('video_limit',)


if not is_registered(UserPlanModel):
    @admin.register(UserPlanModel)
    class UserPlanModelAdmin(admin.ModelAdmin):
        list_display = ('user', 'bot', 'plan', 'get_expiry_jalali_with_remaining_days', 'volume', 'is_active')
        search_fields = ('user__chat_id', 'user__full_name', 'plan__name_fa', 'plan__name_en')
        list_filter = ('is_active', 'expiry', 'plan')
        list_editable = ('is_active',)

        def get_expiry_jalali_with_remaining_days(self, obj):
            expiry_jalali = datetime.fromgregorian(datetime=obj.expiry).strftime('%Y/%m/%d')
            remaining_days = (obj.expiry - timezone.now()).days
            return f'{expiry_jalali} - {remaining_days} Day'
        get_expiry_jalali_with_remaining_days.short_description = 'Expiry'

