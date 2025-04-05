from django.contrib import admin
from .models import NewsletterSubscription

# Register your models here.
@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date', 'is_active')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_date'
