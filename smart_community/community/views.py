from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Event
from .forms import PostForm
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from .models import UserProfile, Post, Event
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Comment
from .forms import CommentForm

def home(request):
    posts = Post.objects.none()
    events = Event.objects.all()
    
    if request.user.is_authenticated:
        try:
            # Get the current user's profile
            user_profile = UserProfile.objects.get(user=request.user)
            print(f"User Profile: {user_profile}")
            
            # Get all users with matching pincode or town
            matching_users = User.objects.filter(
                Q(userprofile__pincode=user_profile.pincode) |
                Q(userprofile__town=user_profile.town)
            )
            print(f"Matching Users: {matching_users}")
            
            # Get posts from these users
            posts = Post.objects.filter(
                user__in=matching_users
            ).select_related('user').order_by('-timestamp')
            
            # Get events from these users
            events = Event.objects.filter(
                user__in=matching_users
            ).order_by('date')

        
        except UserProfile.DoesNotExist:
            print("UserProfile.DoesNotExist: No profile found for this user.")
            messages.warning(request, "You must complete your profile before accessing the home page.")
            return redirect('login')
        
        except Exception as e:
            print(f"Error: {e}")
    
    else:
        return redirect('login')
    
    return render(request, 'community/home.html', {'posts': posts, 'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})
def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            image = request.FILES.get('image')  # Handle uploaded image
            post =Post.objects.create(title=title, content=content, image=image,user=request.user)
            post.save()
            return redirect('home')  # Re direct after successful post creation
        else:
            form = PostForm()
    else:
        return redirect('login')

    return render(request, 'community/create_post.html', {'form': form})


def entrance_view(request):
    return render(request, 'community/entrance.html')

def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        town = request.POST.get("town")
        password1 = request.POST.get("password")
        password2 = request.POST.get("confirm_password")

        # Check if all fields are filled
        if not all([full_name, username, email, phone, pincode, town, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username already exists
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Check if email already exists
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # Check if phone number already exists
        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered.")
            return redirect('register')

        # Create and save user and profile
        user = User.objects.create_user(username=username, email=email, password=password1)
        user_profile = UserProfile(
            user=user,
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            pincode=pincode,
            town=town
        )
        user_profile.save()

        messages.success(request, "Registration successful. You can now login.")
        return redirect('login')

    return render(request, 'community/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email exists in UserProfile
        try:
            user_profile = UserProfile.objects.get(email=email)
            username = user_profile.username  # Get the corresponding username
        except UserProfile.DoesNotExist:
            username = None
        
        # Authenticate using the username and password
        if username:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
        
    return render(request, 'community/login.html')

def post_update(request):
    return render(request, 'community/post_update.html')

def create_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('description')
            image = request.FILES.get('image')  # Handle uploaded image
            event_detail = Event.objects.create(name=title, description=content, image=image,user=request.user,date=timezone.now())
            event_detail.save()
    else:
        return redirect('community/home.html')
    
    return render(request, 'community/create_event.html')

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.event = event
            comment.save()
            return redirect('event_detail', pk=event.pk)  # Refresh the page

    return render(request, 'event_detail.html', {'event': event, 'comments': comments, 'form': form})