from django.urls import path

from .views import PostListView
# from .views import ShareView
from . import views
app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path('share/', views.post_new, name='post_new'),
    path('update/<int:id>/', views.update_post, name='update_post'),
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
    path('like/<int:id>/', views.like_post, name='like_post'),
]
