from django.contrib import admin
from .models import MediaFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "owner", "created_at")
    list_filter = ("created_at", "owner")
    search_fields = ("owner__username",)
    readonly_fields = ("id", "created_at")
    ordering = ("-created_at",)
