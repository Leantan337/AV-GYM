from django.db import models
from django.utils import timezone

# Create your models here.

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
