from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post, Event
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

import requests

GOOGLE_MAPS_API_KEY = "11a6be456a3eee97abd551370de2eb3a"

def get_city_from_coords(latitude, longitude):
    geocode_url = f"https://api.ipstack.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(geocode_url).json()
    
    city = None
    for result in response.get("results", []):
        for component in result.get("address_components", []):
            if "locality" in component["types"]:
                city = component["long_name"]
                break
        if city:
            break

    return city

def home(request):
    posts = Post.objects.all()
    events = Event.objects.all()
    return render(request, 'community/home.html', {'posts': posts, 'events': events})

def event_detail(request, pk):
    return render(request, 'community/event_detail.html', {'event': event})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community/home.html')
    else:
        form = PostForm()
    return render(request, 'community/create_post.html', {'form': form})

def entrance_view(request):
    return render(request, 'community/entrance.html')

from .models import CustomUser
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["confirm_password"]

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('/register')

        # Create and save user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.first_name = full_name
        user.save()
        messages.success(request, "Registration successful. You can now login.")
        return redirect('/register')

    return render(request, 'community/register.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
        
    else:
        return render(request, 'community/login.html')


def post_update(request):
    return render(request, 'community/post_update.html')
