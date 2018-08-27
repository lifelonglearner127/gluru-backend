from os.path import basename
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .models import (
    Ticket, Answer, TicketProduct, TicketHistory,
    TicketNotification, NotficationContact, TicketAttachment
)


class AnswerInlineAdmin(admin.StackedInline):
    model = Answer
    extra = 0
    fields = ['created_by', 'body', 'privacy', 'is_deleted']


class TicketsHistoryInlineAdmin(admin.StackedInline):
    model = TicketHistory
    extra = 0
    fields = ['changed_by', 'changed_field', 'before_value', 'after_value']


class TicketAttachmentInlineAdmin(admin.TabularInline):
    model = TicketAttachment
    extra = 0
    readonly_fields = ['filename', 'created_by', 'is_deleted']
    fields = ['filename', 'created_by', 'is_deleted']

    def filename(self, obj):
        return basename(obj.file.name)
    filename.short_description = 'File name'
    filename.allow_tags = True


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ['answer', 'ticket']
    list_display = ('id', 'file')
    ordering = ['-id']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'status', 'issue_type', 'created_by',
        'assignee', 'updated_by', 'category', 'created_at',
        'updated_at', 'is_activated', 'activate_ticket'
    )

    search_fields = (
        'status', 'title', 'body'
    )

    list_filter = (
        'category', 'issue_type', 'status', 'is_deleted', 'is_private'
    )

    list_display_links = ['title', ]

    inlines = [
        AnswerInlineAdmin, TicketsHistoryInlineAdmin,
        TicketAttachmentInlineAdmin
    ]

    fieldsets = (
        (_('Base'), {
            'fields': (
                ('title'),
                ('body'),
                ('status', 'issue_type', 'category'),
                ('created_by', 'created_for', 'company'),
                ('updated_by', 'is_notified'),
                ('assignee'),
                ('link'),
            )
        }),
        (_('Status'), {
            'fields': ('is_deleted', 'is_private'),
        }),
        (_('Installation Info'), {
            'fields': (
                ('os_type', 'ram'),
                ('os_version', 'os_version_name'),
                ('server_version', 'server_version_comments')
            )
        }),
    )

    class Media:
        js = ('admin/js/custom.js',)

    def activate_ticket(self, obj):
        if obj.is_deleted:
            button_name = 'Activate'
        else:
            button_name = 'Deactivate'

        return mark_safe(
            '<a type="button" href="javascript:void(0);" \
            class="activate_ticket" data-id="{0}" data-action="{1}">{1}</a>'
            .format(obj.id, button_name)
        )

    def is_activated(self, obj):
        return not obj.is_deleted

    is_activated.short_description = 'Is Activated?'
    is_activated.boolean = True

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ticket', 'privacy', 'created_by', 'created_at',
        'updated_at', 'is_deleted'
    )

    search_fields = ('answer',)

    list_filter = ('privacy', 'is_deleted')

    list_display_links = ['ticket', ]

    fieldsets = (
        (_('Base'), {'fields': (
            ('body'),
            ('ticket',),
            ('created_by', 'link_url'))}),
        ('Status', {
            'fields': (('is_deleted',),)
        }),
    )

    inlines = [TicketAttachmentInlineAdmin]


@admin.register(TicketProduct)
class TicketProductAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'ticket', 'changed_by', 'changed_field', 'created_at'
    )

    search_fields = ('ticket', 'chaged_field')

    list_display_links = ['ticket', ]

    readonly_fields = (
        'ticket', 'changed_by', 'changed_field',
        'before_value', 'after_value'
    )


@admin.register(NotficationContact)
class NotficationContactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'number', 'priority', 'enabled'
    )


@admin.register(TicketNotification)
class TicketNotificationAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'is_subscribed', 'created_at')
    search_fields = ('ticket', 'user')
    list_display_links = ['ticket']
