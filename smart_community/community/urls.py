from django.urls import path
from . import views
from .views import entrance_view

urlpatterns = [
    path('', views.home, name='home'),
    path('entrance/', entrance_view, name='entrance'),
    path('Register/', views.Register, name='Register'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('create_post/', views.create_post, name='create_post'),
    path('signup/', views.signup, name='signup'),
]