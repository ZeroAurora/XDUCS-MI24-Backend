from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "content", "notification_type", "created_at", "is_read"]
    list_filter = ["notification_type", "is_read", "created_at"]
    search_fields = ["user__username", "content__content"]
    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    mark_as_unread.short_description = "Mark selected notifications as unread"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "content")
