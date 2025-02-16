from django.db import models
from django.contrib.auth.models import User

class Consultation(models.Model):
    CONSULTATION_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=CONSULTATION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"
