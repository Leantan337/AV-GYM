from django.shortcuts import render, redirect
from blog.models import BlogPage, BlogCategory

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
