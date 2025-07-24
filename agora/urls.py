from django.urls import path
from .views import generate_agora_token, home,call_room  # import all required views

urlpatterns = [
    path('', home, name='home'),  # renders index.html at root URL
    path('get_token/', generate_agora_token, name='generate_agora_token'),
    path('call/<str:channel_name>/', call_room, name='call_room'),
]
