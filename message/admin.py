from django.contrib import admin
from message.models import Message, UserStatus


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "timestamp", "is_read", "is_delivered")
    list_filter = ("is_read", "is_delivered", "timestamp")
    search_fields = ("sender__username", "recipient__username", "content")
    date_hierarchy = "timestamp"


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ("user", "is_online", "is_typing", "last_seen")
    list_filter = ("is_online", "is_typing")
    search_fields = ("user__username",)
