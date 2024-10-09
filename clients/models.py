from django.db import models
from utils import IsActiveModel
from multiselectfield import MultiSelectField


class Client(IsActiveModel):
    name = models.CharField(max_length=255, unique=False)
    rut = models.CharField(max_length=255, unique=True)

    def __str__(self):  
        return self.name

class Message(IsActiveModel):
    client = models.ForeignKey(
        Client, related_name="messages", on_delete=models.CASCADE    
    )
    ROLE_CHOICES = [
        ("client", "client"),
        ("agent", "agent"),
    ]

    text = models.CharField(max_length=255, unique=False)
    role = models.CharField(choices=ROLE_CHOICES, max_length=100, blank=True, null=True)
    sentAt = models.DateTimeField()

class Deudas(IsActiveModel):
    client = models.ForeignKey(
        Client, related_name="debts", on_delete=models.CASCADE
    )
    institution = models.CharField(max_length=255, unique=False)
    amount = models.IntegerField()
    dueDate = models.DateTimeField()
