from django.urls import re_path
from django.urls import include, path

urlpatterns = [
    path("oauth/", include("oauth.urls")),
]
