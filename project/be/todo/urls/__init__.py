from django.urls import path, include

urlpatterns = [
    path('', include('todo.urls.web')),
    path('api/', include('todo.urls.api'))
]
