from django.urls import path

from .views import PostListView
# from .views import ShareView
from . import views
app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path('share/', views.post_new, name='post_new'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('rate/<int:post_id>/', views.rate_post, name='rate_post'),
]
