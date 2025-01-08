from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("users/", include("user.urls")),
    path("posts/", include("post.urls")),
    path("files/", include("file.urls")),
    path("notifications/", include("notification.urls")),
]
