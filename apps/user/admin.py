from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission

from apps.core import apps_config
from .forms import UserChangeForm, UserCreationForm
from .models import User

for model in apps.get_app_config('user').models.values():
    admin.site.register(model)

admin.site.unregister(User)


# admin.site.unregister(Permission)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    search_fields = ['email', 'first_name', 'last_name', 'is_admin', 'is_active']
    list_display = ('email', 'phone', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active',)

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password', ('first_name', 'last_name'),)}),
        ('Biographical Details', {
            # 'classes': ('collapse',),
            'fields': ('avatar',)
        }),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Time', {'fields': ('last_login', 'created_at', 'updated_at')}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()


class UserPermission(admin.ModelAdmin):
    def get_queryset(self, request):
        return apps_config.app_permissions()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# admin.site.register(Permission, UserPermission)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
