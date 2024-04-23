from django.db import models
from django.contrib.auth.models import User
import shortuuid


# Chat group model
class Chatroom(models.Model):
    name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    usersOnline = models.ManyToManyField(User, related_name="online_in_groups", blank=True)
    members = models.ManyToManyField(User, related_name="chat_rooms", blank=True)
    is_private = models.BooleanField(default=False)
    is_group = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
   
# Chat message model 
class ChatMessage(models.Model):
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    # Order messages by 'created' field
    class Meta:
        ordering = ['-created']