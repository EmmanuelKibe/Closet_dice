from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import ClothingItemForm
from .weather_service import fetch_weekly_forecast, determine_weather_suitability
from .models import UserProfile, ClothingItem, WeeklySchedule
from datetime import date, timedelta
from .generator import generate_weekly_wardrobe

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

    # Check if we need to populate empty weather placeholders
    if schedule.monday_weather == "Awaiting forecast...":
        # Get user's city from onboarding profile data (default to Nairobi if empty)
        user_profile = getattr(request.user, 'userprofile', None)
        city = user_profile.location if user_profile and user_profile.location else "Nairobi"
        
        forecast_days = fetch_weekly_forecast(city, settings.VISUAL_CROSSING_API_KEY)
        
        # If the API returned valid data, map the first 5 days to Mon-Fri
        if forecast_days:
            try:
                schedule.monday_weather = determine_weather_suitability(forecast_days[0]['tempmax'])
                schedule.tuesday_weather = determine_weather_suitability(forecast_days[1]['tempmax'])
                schedule.wednesday_weather = determine_weather_suitability(forecast_days[2]['tempmax'])
                schedule.thursday_weather = determine_weather_suitability(forecast_days[3]['tempmax'])
                schedule.friday_weather = determine_weather_suitability(forecast_days[4]['tempmax'])
                schedule.save()
            except (IndexError, KeyError):
                pass
    
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
        form = ClothingItemForm(request.POST, request.FILES)
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
    
@login_required
@require_POST
def roll_wardrobe(request):
    """
    POST handler that triggers the randomizer engine for the active week's schedule.
    """
    today = date.today()
    monday_start = today - timedelta(days=today.weekday())
    
    # Locate the active schedule row for this user
    schedule = WeeklySchedule.objects.filter(user=request.user, week_start_date=monday_start).first()
    
    if schedule:
        generate_weekly_wardrobe(request.user, schedule)
        
    return redirect('dashboard')    