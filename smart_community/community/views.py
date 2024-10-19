from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post, Event
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

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
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'community/create_post.html', {'form': form})

def entrance_view(request):
    return render(request, 'community/entrance.html')

def register(request):
    return render(request, 'community/register.html')

def login(request):
    return render(request, 'community/login.html')

def post_update(request):
    return render(request, 'community/post_update.html')