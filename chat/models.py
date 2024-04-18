from django.db import models
from django.contrib.auth.models import User
import shortuuid


# Chat group model
class ChatGroup(models.Model):
    groupName = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    usersOnline = models.ManyToManyField(User, related_name="online_in_groups", blank=True)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.groupName
    
   
# Chat message model 
class ChatMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    # Order messages by 'created' field
    class Meta:
        ordering = ['-created']