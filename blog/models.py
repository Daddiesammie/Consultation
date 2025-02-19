from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.email

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')
    content = models.TextField()
    excerpt = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = NewsletterSubscriber.objects.filter(
            is_active=True,
            categories__in=[instance.category]
        ).distinct()

        for subscriber in subscribers:
            context = {
                'post': instance,
                'subscriber': subscriber,
            }
            html_message = render_to_string('blog/emails/new_post_notification.html', context)
            
            send_mail(
                subject=f'New Post: {instance.title}',
                message=f'New post in {instance.category}: {instance.title}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                html_message=html_message
            )
