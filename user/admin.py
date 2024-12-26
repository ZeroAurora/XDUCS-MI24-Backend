from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Follower


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_select_related = ("profile",)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed", "created_at")
    list_filter = ("created_at",)
    search_fields = ("follower__username", "followed__username")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
