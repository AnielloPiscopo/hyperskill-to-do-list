from django.urls import path, include

urlpatterns = [
    path('web/', include('todo.urls.web')),
    path('api/', include('todo.urls.api'))
]
