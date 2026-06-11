from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(name_or_request, *args, **kwargs):
    # This ensures it works whether called normally or with arguments
    request = name_or_request if not isinstance(name_or_request, str) else args[0]
    # The @login_required decorator ensures that if a user is NOT logged in,
    # they are automatically redirected to our beautiful login page.
    return render(request, 'core/dashboard.html')
