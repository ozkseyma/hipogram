from django.db import models


class Thread(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="+")
    receiver = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="+")


class Message(models.Model):
    sender = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="receiver")
    thread = models.ForeignKey("Thread", related_name="+", on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
