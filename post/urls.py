from django.urls import include, path
from post.views import (
    CreatePost,
    DeletePost,
    ReadPost,
    ReadPosts,
    SearchPosts,
    UpdatePost,
)

urlpatterns = [
    path("all", ReadPosts.as_view(), name="read posts"),
    path("create", CreatePost.as_view(), name="create post"),
    path("read", ReadPost.as_view(), name="read post"),
    path("update", UpdatePost.as_view(), name="update post"),
    path("delete", DeletePost.as_view(), name="delete post"),
    path("search", SearchPosts.as_view(), name="search post"),
    path("comment/", include("comment.urls")),
    path("like/", include("postlike.urls")),
]