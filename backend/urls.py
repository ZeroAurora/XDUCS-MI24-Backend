from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from user.views import ProfileViewSet
from post.views import ContentViewSet
from file.views import MediaFileViewSet
from notification.views import NotificationViewSet

router = routers.DefaultRouter()

router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"posts", ContentViewSet, basename="post")
router.register(r"files", MediaFileViewSet, basename="mediafile")
router.register(r"notifications", NotificationViewSet, basename="notification")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
