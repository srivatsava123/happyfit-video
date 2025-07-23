from django.urls import path
from .views import generate_agora_token

urlpatterns = [
    path('get_token/', generate_agora_token),
]
