from django.urls import path
from .views import entrance_view
from community import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', entrance_view, name='entrance'),
    # path('event/<int:pk>/', views., name='event_detail'),
    path('create_post/', views.create_post, name='create_post'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('post_update/', views.post_update, name='post_update'),
]