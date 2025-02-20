
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    pincode = models.CharField(max_length=6)
    town = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} - {self.town}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post by {self.user.username} at {self.timestamp}"

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events',null=True, blank=True)
    name = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.name} on {self.date}"



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:30]}"