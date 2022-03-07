from django.urls import path

from .views import SignUpView, LogInView, LogOutView, EditProfileView, MessageView

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("users/edit-profile/<int:user_id>", EditProfileView.as_view(), name="edit"),
    path("messages/<int:user_id>", MessageView.as_view(), name="message"),
]
