from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from user import views as user_views
from post import views as post_views
from django.contrib import admin

router = DefaultRouter()
router.register(r"users", user_views.UserViewSet, basename="user")
router.register(r"posts", post_views.PostViewSet, basename="post")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", obtain_auth_token, name="api_token_auth"),
    path("", include(router.urls)),
]
