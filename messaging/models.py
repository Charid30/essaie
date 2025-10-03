from django.db import models
from users.models import User

class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    MESSAGE_TYPES = (
        ('texte', 'Texte'),
        ('image', 'Image'),
        ('appel', 'Appel'),
    )
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='texte')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
