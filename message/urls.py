from django.urls import path, include
from rest_framework.routers import DefaultRouter
from message import views

router = DefaultRouter()
router.register(r"messages", views.MessageViewSet, basename="message")
router.register(r"status", views.UserStatusViewSet, basename="user-status")

urlpatterns = [
    path("", include(router.urls)),
]
