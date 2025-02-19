from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import entrance_view
from community import views
from .views import event_detail

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', entrance_view, name='entrance'),
    path('event/<int:pk>/', event_detail, name='event_detail'), 
    path('create_post/', views.create_post, name='create_post'),
    path('create_event/', views.create_event, name='create_event'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('post_update/', views.post_update, name='post_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
