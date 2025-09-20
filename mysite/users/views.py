# views.py for a typical Django user application

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# --- User Registration View ---
def register_view(request):
    """
    Handles user registration.
    If the request method is POST, it attempts to create a new user.
    Otherwise, it displays an empty registration form.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, "Registration successful. Welcome!")
            return redirect('dashboard')  # Redirect to a profile page or dashboard
        else:
            # If form is not valid, add error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# --- User Login View ---
def login_view(request):
    """
    Handles user login.
    If the request method is POST, it attempts to authenticate the user.
    Otherwise, it displays an empty login form.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')  # Redirect to a profile page or dashboard
            else:
                messages.error(request, "Account does not exist")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# --- User Logout View ---
@login_required # Ensures only logged-in users can access this view
def logout_view(request):
    """
    Logs out the current user and redirects to the login page or homepage.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login') # Redirect to login page after logout

# --- User Profile View ---
@login_required # Ensures only logged-in users can access this view
def profile_view(request):
    """
    Displays the current user's profile information.
    This view requires the user to be logged in.
    """
    # You can pass user-specific data to the template here
    # For example, if you have a custom UserProfile model:
    # try:
    #     user_profile = request.user.userprofile
    # except UserProfile.DoesNotExist:
    #     user_profile = None # Or create a default profile

    context = {
        'user': request.user,
        # 'user_profile': user_profile, # Uncomment if you have a UserProfile model
    }
    return render(request, 'users/profile.html', context)

# --- Example of a protected dashboard view ---
@login_required
def dashboard_view(request):
    """
    An example of a view that requires user authentication to access.
    """
    return render(request, 'users/dashboard.html', {'message': 'Welcome to your dashboard!'})

# --- Password Change View (using Django's built-in views) ---
# For password change, it's often better to use Django's built-in views
# from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
# You would typically configure these in your urls.py directly.
# Example:
# from django.urls import path
# from django.contrib.auth import views as auth_views
#
# urlpatterns = [
#     path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
#     path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
# ]
