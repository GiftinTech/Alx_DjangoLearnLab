from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Handles user registration
# - Displays a registration form (GET request)
# - Saves new user and logs them in automatically (POST request)

def register_view(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)  # Log in user after registration
      return redirect('profile')
  else:
    form = RegisterForm()
  return render(request, 'registration/register.html', {'form': form})

@login_required

# Handles user profile view & update
# - Requires login to access (@login_required)
# - Allows updating email address
@login_required
def profile_view(request):
  if request.method == 'POST':
    request.user.email = request.POST.get('email')
    request.user.save()
  return render(request, 'registration/profile.html')
