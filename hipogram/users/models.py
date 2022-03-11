from django.db import models
from django.contrib.auth.models import User
from itertools import chain


class UserMethods(User):

    @property
    def message_count(self):
        return chain(self.received_messages, self.sent_messages).count()

    class Meta:
        proxy = True


class Message(models.Model):
    sender = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="sent_messages")
    receiver = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="received_messages")
    text = models.CharField(max_length=2000)
    creation_datetime = models.DateTimeField(auto_now_add=True)
