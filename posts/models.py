from django.db import models
from django.contrib.auth.models import User 

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField() 
    date_posted = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Post by {self.author.username}"