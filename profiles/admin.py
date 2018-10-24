from django.contrib import admin
from profiles.models import User


@admin.register(User)
class SupportUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name',
        'last_name', 'is_staff', 'is_active'
    )
    ordering = ('-id',)
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'phone_number'
        )}),
        ('Permissions', {'fields': ('is_staff', )}),
        ('Additional Info', {'fields': (
            'is_active', 'created_at', 'idp_uuid'
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ()
    list_filter = ()
