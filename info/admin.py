from django.contrib import admin
from info.models import (
    GluuServer, GluuProduct, GluuOS, TicketCategory, TicketIssueType
)


@admin.register(GluuServer)
class GluuServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(GluuProduct)
class GluuProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(GluuOS)
class GluuOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(TicketIssueType)
class TicketIssueTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'priority')
