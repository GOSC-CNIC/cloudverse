from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile, Email


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ('id', 'username', 'fullname', 'company', 'telephone', 'is_active', 'is_staff', 'date_joined')
    list_display_links = ('id', 'username')
    # list_filter = ('date_joined', 'is_superuser', 'is_staff')
    search_fields = ('username', 'company', 'first_name', 'last_name')  # 搜索字段

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('个人信息'), {'fields': ('first_name', 'last_name', 'email', 'company', 'telephone')}),
        (_('权限信息'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('date_joined',)}),
    )
    ordering = None

    def fullname(self, obj):
        return obj.get_full_name()

    fullname.short_description = _('姓名')


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'sender', 'receiver', 'send_time', 'message')
    list_display_links = ('id', 'subject')
    search_fields = ('subject', 'receiver')
