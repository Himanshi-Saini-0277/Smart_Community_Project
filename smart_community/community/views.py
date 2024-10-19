from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post, Event
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import subprocess
from django.http import JsonResponse
import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sys

def home(request):
    posts = Post.objects.all()
    events = Event.objects.all()
    return render(request, 'community/home.html', {'posts': posts, 'events': events})

def post_update(request):
    return render(request, 'community/post_update.html')

def create_post(request):
    return render(request, 'community/create_post.html')

def entrance_view(request):
    return render(request, 'community/entrance.html')

def register(request):
    return render(request, 'community/register.html')

def login(request):
    return render(request, 'community/login.html')

def collect_data(request):
    if request.method == 'POST':
        try:
            # Get the house number from the request body
            data = json.loads(request.body)
            house_number = data.get('house_number')

            if not house_number:
                return JsonResponse({'success': False, 'error': 'House number not provided'})

            # Run the collect_data.py script with the house number
            subprocess.run(["python3", "path/to/collect_data.py", house_number], check=True)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt  # If using POST, make sure CSRF tokens are handled correctly

def capture_image(request):
    if request.method == 'POST':
        house_number = request.POST.get('house_number')

        if house_number:
            try:
                print("Python executable:", sys.executable)
                script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'collect_data.py')
                result = subprocess.run(
                    [sys.executable, script_path, house_number],
                    check=True,
                    text=True,
                    capture_output=True
                )

                # Print output and error for debugging
                print("STDOUT:", result.stdout)  # Standard output from the script
                print("STDERR:", result.stderr)  # Standard error output

                return render(request, 'community/success.html', {'house_number': house_number})
            except subprocess.CalledProcessError as e:
                print("Error occurred while executing the script:", e)  # Log error information
                print("Error Output:", e.stderr)  # Print specific error messages
                return render(request, 'community/error.html', {'error': 'Failed to collect data: ' + str(e)})

    return render(request, 'community/create_post.html')