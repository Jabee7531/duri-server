from django.urls import path
from postlike.views import CreatePostLike, DeletePostLike

urlpatterns = [
    path("create", CreatePostLike.as_view(), name="create postlike"),
    path("delete", DeletePostLike.as_view(), name="delete postlike"),
]
