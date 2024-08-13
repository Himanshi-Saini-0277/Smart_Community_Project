from django.contrib import admin

# Register your models here.
from .models import Post, Event, Comment, Notification

admin.site.register(Post)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Notification)