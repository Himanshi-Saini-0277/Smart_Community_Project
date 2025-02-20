from django.contrib import admin
from .models import UserProfile, Post, Event, Comment

# Utility function to get user's pincode and town
def get_user_location(obj):
    if obj.user and hasattr(obj.user, 'userprofile'):
        return f"{obj.user.userprofile.pincode}, {obj.user.userprofile.town}"
    return "N/A"

get_user_location.short_description = "Location"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'phone', 'pincode', 'town')
    search_fields = ('username', 'full_name', 'email', 'phone', 'pincode', 'town')
    list_filter = ('town', 'pincode')
    ordering = ('username',)
    readonly_fields = ('user',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'user_location', 'timestamp', 'image_preview')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def user_location(self, obj):
        return get_user_location(obj)
    user_location.short_description = "Location"

    def image_preview(self, obj):
        if obj.image:
            return f"✅ <a href='{obj.image.url}' target='_blank'>View</a>"
        return "❌ No Image"
    image_preview.short_description = "Image"
    image_preview.allow_tags = True

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'user_location', 'date', 'description_short', 'image_preview')
    search_fields = ('name', 'description', 'user__username')
    list_filter = ('date',)
    ordering = ('date',)

    def user_location(self, obj):
        return get_user_location(obj)
    user_location.short_description = "Location"

    def description_short(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_short.short_description = "Short Description"

    def image_preview(self, obj):
        if obj.image:
            return f"✅ <a href='{obj.image.url}' target='_blank'>View</a>"
        return "❌ No Image"
    image_preview.short_description = "Image"
    image_preview.allow_tags = True

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'timestamp')
    search_fields = ('author__username', 'post__title', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Comment Preview"
