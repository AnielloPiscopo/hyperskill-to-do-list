from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]