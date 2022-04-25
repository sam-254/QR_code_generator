from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, RedirectView
from .forms import SignupForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserInfoForm
from django.contrib import messages
from .utils import generate_user_qr
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic import RedirectView


User = get_user_model()


class SignupView(FormView):
    """sign up user view"""
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user_info')

    def form_valid(self, form):
        """ process user signup"""
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)


class LoginView(FormView):
    """login view"""

    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data
        user = authenticate(self.request, username=credentials["email"], password=credentials["password"])
        if user:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login'))


class LogoutView(RedirectView):
    """
    A view that logout user and redirect to homepage.
    """
    permanent = False
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class UserInfoView(LoginRequiredMixin, View):
    """
    User Info submission processes.
    """
    login_url = '/login/'
    template_name = 'user_info.html'
    form_class = UserInfoForm
    success_url = '/generate/'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class HomeView(ListView):
    """
    Listing users with QR code.
    """
    model = User
    template_name = "home.html"
    context_object_name = "users"


class GenerateQrView(LoginRequiredMixin, View):
    """
    Generating QR code for user.
    """
    login_url = '/login/'
    template_name = 'generate_qr.html'
    success_url = '/home/'

    def post(self, request):
        image_path = request.POST.get("img_path")
        if image_path is None:
            pass
        request.user.qr_img = image_path
        request.user.save()
        return redirect("/home/")

    def get(self, request):
        username = request.user.get_username()
        phone = request.user.phone
        email = request.user.email
        img_path, img_url = generate_user_qr(username, phone, email)
        context = {
            'img_url': img_url,
            'img_path': img_path,
        }

        return render(request, 'user_qr.html', context)




