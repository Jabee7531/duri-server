from django.urls import path
from .views import CreateComment, DeleteComment, ReadComments, UpdateComment

urlpatterns = [
    path("create", CreateComment.as_view(), name="create commtents"),
    path("all", ReadComments.as_view(), name="read commtents"),
    path("update", UpdateComment.as_view(), name="update commtents"),
    path("delete", DeleteComment.as_view(), name="delete commtents"),
]
