from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class VideoCallSession(models.Model):
    channel_name = models.CharField(max_length=100, unique=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='video_sessions', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.channel_name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
