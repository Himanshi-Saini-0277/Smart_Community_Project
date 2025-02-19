from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)
    postal_area = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.postal_area}"

class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    image = models.TextField()


    def __str__(self):
        return f"Post by {self.user.user.username} at {self.timestamp}"

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()


    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
