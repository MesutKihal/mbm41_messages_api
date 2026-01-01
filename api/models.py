from django.db import models


class Sender(models.Model):
    full_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content
