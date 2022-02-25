from django.urls import path

from .views import PostListView, PostCreateView, PostDeleteView, PostUpdateView, LikeView, RateView
app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("share/", PostCreateView.as_view(), name="share"),
    path("delete/<int:post_id>/", PostDeleteView.as_view(), name="delete"),
    path("update/<int:post_id>/", PostUpdateView.as_view(), name="update"),
    path("like/<int:post_id>/", LikeView.as_view(), name="like"),
    path("rate/<int:post_id>/", RateView.as_view(), name="rate"),
]
