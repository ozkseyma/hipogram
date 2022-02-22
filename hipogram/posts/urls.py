from django.urls import path

from .views import PostListView, PostCreateView, PostDeleteView, PostUpdateView
from . import views
app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path('share/', PostCreateView.as_view(), name='share'),
    path('delete/<int:post_id>/', PostDeleteView.as_view(), name='delete'),
    path('update/<int:post_id>/', PostUpdateView.as_view(), name='update'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('rate/<int:post_id>/', views.rate_post, name='rate_post'),
]
