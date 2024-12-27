from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", obtain_auth_token, name="api_token_auth"),
    path("users/", include("user.urls")),
    path("posts/", include("post.urls")),
    path("chat/", include("message.urls")),
    path("files/", include("file.urls")),
    path("api-schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
