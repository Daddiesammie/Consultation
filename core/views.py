from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Award, Service, Portfolio, TeamMember, Testimonial, Contact
from .forms import ContactForm
from urllib.parse import urlparse, parse_qs
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def get_youtube_embed_url(url):
    """Convert YouTube URL to embed URL"""
    if 'youtube.com' in url or 'youtu.be' in url:
        parsed_url = urlparse(url)
        if 'youtu.be' in url:
            # Extract video ID from youtu.be URL
            video_id = parsed_url.path.split('/')[1].split('?')[0]
        else:
            # Extract video ID from youtube.com URL
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
    return url


def home(request):
    featured_projects = Portfolio.objects.filter(is_featured=True)[:3]
    services = Service.objects.all()[:6]
    testimonials = Testimonial.objects.all()[:3]
    
    for project in featured_projects:
        if project.video_url:
            project.embed_url = get_youtube_embed_url(project.video_url)

    context = {
        'featured_projects': featured_projects,
        'services': services,
        'testimonials': testimonials,
    }
    return render(request, 'core/home.html', context)

def about(request):
    testimonials = Testimonial.objects.all()
    team_members = TeamMember.objects.all().order_by('order')
    awards = Award.objects.all().order_by('-date_received')
    
    context = {
        'testimonials': testimonials,
        'team_members': team_members,
        'awards': awards,
    }
    
    return render(request, 'core/about.html', context)


def services(request):
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()[:3]
    context = {
        'services': services,
        'testimonials': testimonials,
    }
    return render(request, 'core/services.html', context)

def portfolio(request):
    portfolio_items = Portfolio.objects.all()
    
    for item in portfolio_items:
        if item.video_url:
            item.embed_url = get_youtube_embed_url(item.video_url)
    
    context = {
        'portfolio': portfolio_items,
    }
    return render(request, 'core/portfolio.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email to admin
            admin_context = {
                'name': contact.name,
                'email': contact.email,
                'subject': contact.subject,
                'message': contact.message,
                'created_at': contact.created_at
            }
            
            admin_email_html = render_to_string('core/emails/admin_contact_notification.html', admin_context)
            send_mail(
                f'New Contact Form Submission: {contact.subject}',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                html_message=admin_email_html
            )
            
            # Send confirmation email to user
            user_context = {
                'name': contact.name,
                'subject': contact.subject
            }
            
            user_email_html = render_to_string('core/emails/user_contact_confirmation.html', user_context)
            send_mail(
                'Thank you for contacting Dan & Dave Consulting Ltd',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [contact.email],
                html_message=user_email_html
            )
            
            messages.success(request, 'Your message has been sent successfully! Check your email for confirmation.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)

def portfolio_detail(request, pk):
    project = get_object_or_404(Portfolio, pk=pk)
    related_projects = Portfolio.objects.exclude(pk=pk)[:3]
    
    # Clean video URL to get embed format
    if project.video_url:
        video_id = project.video_url.split('?')[0].split('/')[-1]
        project.embed_url = f"https://www.youtube.com/embed/{video_id}"
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'core/portfolio_detail.html', context)

def privacy_policy(request):
    return render(request, 'core/privacy-policy.html')

def terms_of_service(request):
    return render(request, 'core/terms-of-service.html')

def faq(request):
    return render(request, 'core/faq.html')

def cookie_policy(request):
    return render(request, 'core/cookie_policy.html')
