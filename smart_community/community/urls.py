from django.urls import path
from . import views
from .views import entrance_view
from .views import register
from .views import login
from .views import post_update
from .views import collect_data

urlpatterns = [
    path('', views.home, name='home'),
    path('entrance/', entrance_view, name='entrance'),
    path('post_update/', post_update, name='post_update'),
    path('create_post/', views.create_post, name='create_post'),
    path('collect_data/', collect_data, name='collect_data'),
    path('capture-image/', views.capture_image, name='capture_image'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]