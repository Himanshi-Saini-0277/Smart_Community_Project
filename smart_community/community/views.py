from django.shortcuts import render, redirect

# Create your views here.
from .models import Post, Event
from .forms import PostForm
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UserProfile
from django.db import models

def home(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        posts = Post.objects.filter(models.Q(user__postal_code=user_profile.postal_code) | models.Q(user__area_name=user_profile.area_name))
        events = Event.objects.filter(models.Q(user__postal_code=user_profile.postal_code) | models.Q(user__area_name=user_profile.area_name))
    else:
        posts = Post.objects.none()
        events = Event.objects.none()

    return render(request, 'community/home.html', {'posts': posts, 'events': events})

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

def register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        postal_code = request.POST['postal_code']
        area_name = request.POST['area_name']
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
