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

@login_required
def profile(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')
        
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'community/profile.html', {'user_posts': user_posts})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'community/signup.html', {'form': form})

def entrance_view(request):
    return render(request, 'community/entrance.html')