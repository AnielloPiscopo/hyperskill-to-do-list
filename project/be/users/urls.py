from .views import RegisterView
from django.urls import path

urlpatterns = [
    path('', RegisterView.as_view()),
]