from django.urls import path
from user import views

urlpatterns = [
    path("<int:pk>/", views.UserProfileView.as_view(), name="user-profile"),
    path("<int:pk>/follow/", views.UserFollowView.as_view(), name="user-follow"),
    path("<int:pk>/unfollow/", views.UserUnfollowView.as_view(), name="user-unfollow"),
    path("<int:pk>/followers/", views.UserFollowersListView.as_view(), name="user-followers"),
    path("<int:pk>/following/", views.UserFollowingListView.as_view(), name="user-following"),
    path("profile/", views.CurrentUserProfileView.as_view(), name="current-user-profile"),
]
