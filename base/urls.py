from django.urls import path
from .views import HomeView, SignupView, LogoutView, LoginView, UserInfoView, GenerateQrView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('user_info/', UserInfoView.as_view(), name='user_info'),
    path('home/', HomeView.as_view(), name='home'),
    path('generate/', GenerateQrView.as_view(), name="generate"),

]
