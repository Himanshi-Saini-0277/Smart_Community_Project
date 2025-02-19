from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Event, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title' ,'content','image')  
    search_fields = ['title'] 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date','description')
    search_fields = ['name']  
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post' ,'content') 
    search_fields = ['post']  
