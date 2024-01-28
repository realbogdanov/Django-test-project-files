from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Profile
from .forms import AvatarUploadForm


class ProfileListView(ListView):
    template_name = "myauth/profile-list.html"
    model = Profile
    context_object_name = "profiles"


class ProfileDetailView(UserPassesTestMixin, DetailView):
    template_name = "myauth/profile-detail.html"
    model = Profile
    context_object_name = "profile"

    def test_func(self):
        user = self.request.user
        profile = self.get_object()
        return user.is_staff or profile.user == user


class AboutMeView(FormView):
    form_class = AvatarUploadForm
    template_name = "myauth/about-me.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        profile.avatar = form.cleaned_data["avatar"]
        profile.save()
        return super().form_valid(form)

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ["avatar", "bio", "agreement_accepted"]
    template_name = "myauth/profile-update.html"
    success_url = reverse_lazy("myauth:about-me")


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
