from django.urls import path
from .views import RegisterView, LoginView, InfoView, LogoutView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('about/', InfoView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]