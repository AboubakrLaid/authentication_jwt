from django.urls import path
from .views import (
    register,
    my_login,
    my_logout,
    home
)

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", my_login, name="login"),
    path("logout/", my_logout, name="logout"),
    path("home/<int:id>", home, name="home")
]
