from django.contrib.auth.views import LoginView
from django.urls import path


from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    ProfileListView,
    ProfileDetailView,
    ProfileUpdateView,
)

app_name = "myauth"

urlpatterns = [
    # path("login/", login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # path("logout/", logout_view, name="logout"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),

    path("profiles/", ProfileListView.as_view(), name="profiles-list"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-details"),
    path("profiles/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),

    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]
