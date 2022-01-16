from django.urls import path

from .views import PostListView
#from .views import ShareView
from . import views
app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    #path("", ShareView.as_view(), name="share"),
    path('share/', views.post_new, name='post_new'),
]