from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import EmailVerificationToken, User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (('Role', {'fields': ('role',)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (('Role', {'fields': ('email', 'role')}),)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(ModelAdmin):
    list_display = ('user', 'is_verified', 'attempts', 'sent_at', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'token', 'code_hash', 'attempts', 'sent_at', 'created_at')
    fields = ('user', 'is_verified', 'attempts', 'sent_at', 'created_at')
