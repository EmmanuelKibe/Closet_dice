from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import ClothingItemForm
from .models import UserProfile, ClothingItem, WeeklySchedule
from datetime import date, timedelta

@login_required
def dashboard(request):
    # 1. Calculate the calendar date of the current week's Monday
    today = date.today()
    monday_start = today - timedelta(days=today.weekday())
    
    # 2. Grab the existing schedule or create a fresh blank one for this user
    schedule, created = WeeklySchedule.objects.get_or_create(
        user=request.user,
        week_start_date=monday_start
    )
    
    context = {
        'schedule': schedule,
        'week_start': monday_start,
        'week_end': monday_start + timedelta(days=4)  # Friday's date boundary
    }
    return render(request, 'core/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 1. Save the new user to the database
            user = form.save()
            
            # 2. Automatically create their empty UserProfile
            UserProfile.objects.create(user=user)
            
            # 3. Instantly log the user in behind the scenes
            login(request, user)
            
            # 4. Redirect them to the main dashboard
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})

@login_required
def upload_clothing(request):
    # Detect if the device is a mobile phone using HTTP headers
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile = any(device in user_agent for device in ['iphone', 'android', 'blackberry', 'mobile'])

    if request.method == 'POST':
        form = ClothingItemForm(request.POST)
        if form.is_valid():
            # Create the item but don't save to the database just yet
            clothing_item = form.save(commit=False)
            # Tie the clothing item explicitly to the active logged-in user
            clothing_item.user = request.user
            clothing_item.save()
            return redirect('dashboard')
    else:
        form = ClothingItemForm()

    context = {
        'form': form,
        'is_mobile': is_mobile
    }
    return render(request, 'core/upload_clothing.html', context)