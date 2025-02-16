from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from consultations.models import Consultation
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from .models import Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Send welcome email
            subject = 'Welcome to D&D Consulting!'
            html_message = render_to_string('accounts/welcome_email.html', {
                'user': user,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                'noreply@danddconsulting.com',
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Registration successful! Welcome email sent.')
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('accounts:dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('core:home')
@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    # Get recent consultations
    consultations = Consultation.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'consultations': consultations,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def settings(request):
    return render(request, 'accounts/settings.html')