from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import ClothingItemForm
from .models import UserProfile, ClothingItem

@login_required
def dashboard(name_or_request, *args, **kwargs):
    # This ensures it works whether called normally or with arguments
    request = name_or_request if not isinstance(name_or_request, str) else args[0]
    # The @login_required decorator ensures that if a user is NOT logged in,
    # they are automatically redirected to the login page.
    return render(request, 'core/dashboard.html')

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