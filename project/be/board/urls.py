from django.urls import path
from .views import BoardDetailView, BoardListView

urlpatterns = [
    path('', BoardListView.as_view()),
    path('<int:pk>/', BoardDetailView.as_view()),
]