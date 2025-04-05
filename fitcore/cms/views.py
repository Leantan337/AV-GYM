from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from blog.models import BlogPage, BlogCategory
from .models import NewsletterSubscription

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    blog_entries = BlogPage.objects.live().order_by('-date')
    categories = BlogCategory.objects.all()
    return render(request, 'blog.html', {
        'blog_entries': blog_entries,
        'categories': categories,
    })

def blog_details(request):
    return render(request, 'blog-details.html')

def class_details(request):
    return render(request, 'class-details.html')

def class_schedule(request):
    return render(request, 'class-schedule.html')

def classes(request):
    return render(request, 'classes.html')

def contact(request):
    return render(request, 'contact.html')

def contact_handler(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('username')
        email = request.POST.get('usermail')
        phone = request.POST.get('userphone')
        message = request.POST.get('usermessage')
        
        # Here you would typically process the form data
        # For example, send an email or save to database
        
        # Redirect to thank you page
        return redirect('cms:thank_you')
    
    # If not POST, redirect back to contact page
    return redirect('cms:contact')

def gallery(request):
    return render(request, 'gallery.html')

def pricing(request):
    return render(request, 'our-pricing.html')

def thank_you(request):
    return render(request, 'thank-you.html')

def trainers(request):
    return render(request, 'trainers.html')

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if email already exists
            if NewsletterSubscription.objects.filter(email=email).exists():
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'exists', 'message': 'You are already subscribed to our newsletter.'})
                messages.info(request, 'You are already subscribed to our newsletter.')
            else:
                # Create new subscription
                NewsletterSubscription.objects.create(email=email)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing to our newsletter!'})
                messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'})
            messages.error(request, 'Please provide a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def search(request):
    query = request.GET.get('search-field', '')
    blog_results = []
    
    if query:
        # Search in blog posts
        blog_results = BlogPage.objects.live().search(query)
    
    return render(request, 'search-results.html', {
        'query': query,
        'blog_results': blog_results,
    })
