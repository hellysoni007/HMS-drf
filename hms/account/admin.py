from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('id', 'email', 'first_name', 'last_name', 'role',)
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        (
        'Personal info', {'fields': ('first_name', 'last_name', 'contact', 'birthdate', 'age', 'joining_date', 'gender',
                                     'qualifications', 'speciality', 'experiance_in_years')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'role', 'first_name')
    ordering = ('email', 'id')
    filter_horizontal = ()

    # Now register the new UserAdmin...


admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
