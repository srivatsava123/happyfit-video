import time
import random
import json
import os

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from agora_token_builder import RtcTokenBuilder
from .models import Trainer, VideoCallSession


@api_view(['POST'])
def generate_agora_token(request):
    """
    Generates Agora token for a given channel name.
    """
    channel_name = request.data.get("channel_name")

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
        "channel_name": channel_name,
        "expire_ts": expire_ts
    })


@csrf_exempt
def schedule_session(request):
    """
    Schedules a new video call session with trainer and timing.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            trainer_username = data.get("trainer")
            start_time = data.get("start_time")  # e.g., "2025-07-24T12:00:00"
            end_time = data.get("end_time")
            channel_name = data.get("channel_name")

            if not (trainer_username and start_time and end_time and channel_name):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            trainer_user = get_object_or_404(User, username=trainer_username)
            trainer, _ = Trainer.objects.get_or_create(user=trainer_user)

            session = VideoCallSession.objects.create(
                trainer=trainer,
                start_time=start_time,
                end_time=end_time,
                channel_name=channel_name
            )

            return JsonResponse({
                "status": "scheduled",
                "channel": session.channel_name,
                "trainer": trainer_username,
                "start_time": start_time,
                "end_time": end_time
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST request required"}, status=405)


def home(request):
    return render(request, 'index.html')
def call_room(request, channel_name):
    return render(request, "room.html", {"channel_name": channel_name})
