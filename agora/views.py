from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from agora_token_builder import RtcTokenBuilder
from django.conf import settings
import time, random
from django.shortcuts import render

@api_view(['POST'])
def generate_agora_token(request):
    channel_name = request.data.get("channel_name")  # ✅ This should read JSON

    if not channel_name:
        return Response({"error": "channel_name is required"}, status=400)

    uid = random.randint(1, 99999)
    expiration = 3600
    current_ts = int(time.time())
    expire_ts = current_ts + expiration

    token = RtcTokenBuilder.buildTokenWithUid(
        settings.AGORA_APP_ID,
        settings.AGORA_APP_CERTIFICATE,
        channel_name,
        uid,
        1,  # Role_Attendee
        expire_ts
    )

    return Response({
        "app_id": settings.AGORA_APP_ID,
        "token": token,
        "uid": uid,
        "channel_name": channel_name,  # ✅ Echo the actual input
        "expire_ts": expire_ts
    })

def home(request):
    return render(request, 'index.html')
