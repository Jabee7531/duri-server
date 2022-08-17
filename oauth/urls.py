from django.urls import path
from .views import UserCheck, UserLogOut, UserSignIn, UserSignUp

urlpatterns = [
    path("check", UserCheck.as_view(), name="check"),
    path("signin", UserSignIn.as_view(), name="signin"),
    path("signup", UserSignUp.as_view(), name="check"),
    path("logout", UserLogOut.as_view(), name="logout"),
]
