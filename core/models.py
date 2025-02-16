from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.company}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.CharField(max_length=100)
    completion_date = models.DateField()
    image = models.ImageField(upload_to='portfolio/')
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completion_date']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    is_key_member = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Award(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField()
    date_received = models.DateField()
    image = models.ImageField(upload_to='awards/')
    certificate_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_received']

    def __str__(self):
        return f"{self.title} - {self.organization}"
