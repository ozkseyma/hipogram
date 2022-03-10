from django.db import models


class Message(models.Model):
    sender = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="sent_messages")
    receiver = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="received_messages")
    text = models.CharField(max_length=2000)
    creation_datetime = models.DateTimeField(auto_now_add=True)
