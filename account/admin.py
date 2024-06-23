from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from account.forms import UserCreationForm, UserChangeForm
from account.models import User
from account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_rel', 'first_name', 'last_name', 'email', 'national_id', 'gender', 'address', 'city', 'province')
    list_filter = ('gender', )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'status', 'account_type', 'is_staff')
    list_filter = ('status', 'account_type', 'is_active')

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'status', 'account_type', 'last_login', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'status', 'account_type', 'is_active', 'is_staff', 'password1', 'password2')}),
    )

    search_fields = ('phone_number', )
    ordering = ('phone_number', )
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)