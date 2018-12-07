from django.contrib import admin
from info import models as m


@admin.register(m.GluuServer)
class GluuServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(m.GluuProduct)
class GluuProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(m.GluuOS)
class GluuOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(m.TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(m.TicketIssueType)
class TicketIssueTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'priority')


@admin.register(m.TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
