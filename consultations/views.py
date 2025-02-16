from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Consultation
from .forms import ConsultationForm

@login_required
def book_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.user = request.user
            consultation.save()

            # Send confirmation email to user
            context = {
                'user': request.user,
                'consultation': consultation,
            }
            
            user_email_html = render_to_string('consultations/emails/user_confirmation.html', context)
            send_mail(
                'Consultation Request Received - D&D Consulting',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                html_message=user_email_html
            )
            
            # Send notification to admin
            admin_email_html = render_to_string('consultations/emails/admin_notification.html', context)
            send_mail(
                'New Consultation Request',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                html_message=admin_email_html
            )

            messages.success(request, 'Consultation request submitted successfully! Check your email for confirmation.')
            return redirect('consultations:my_consultations')
    else:
        form = ConsultationForm()
    
    return render(request, 'consultations/book_consultation.html', {'form': form})

@login_required
def my_consultations(request):
    consultations = Consultation.objects.filter(user=request.user)
    return render(request, 'consultations/my_consultations.html', {'consultations': consultations})
