from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractUser):

    @property
    def message_count(self):
        return self.received_messages.count() + self.sent_messages.count()


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="sent_messages")
    receiver = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="received_messages")
    text = models.CharField(max_length=2000)
    creation_datetime = models.DateTimeField(auto_now_add=True)
