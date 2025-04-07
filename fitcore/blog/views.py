from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import Page
from wagtail.search.models import Query
from .models import BlogPage, BlogCategory

# Create your views here.

def search(request):
    search_query = request.GET.get('query', '')
    
    if search_query:
        search_results = BlogPage.objects.live().search(search_query)
        Query.get(search_query).add_hit()
    else:
        search_results = BlogPage.objects.none()
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(search_results, 10)  # Show 10 results per page
    
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })

def category_view(request, category_slug):
    category = get_object_or_404(BlogCategory, slug=category_slug)
    blog_posts = BlogPage.objects.live().filter(categories__category=category).order_by('-date')
    
    return render(request, 'blog/category.html', {
        'category': category,
        'blog_posts': blog_posts,
    })

def blog_detail(request, post_slug):
    post = get_object_or_404(BlogPage, slug=post_slug)
    recent_posts = BlogPage.objects.live().exclude(id=post.id).order_by('-date')[:5]
    all_categories = BlogCategory.objects.all()
    post_categories = post.categories.all()
    
    # Get the template from the model's method
    template = post.get_template(request)
    
    return render(request, template, {
        'page': post,  # Use 'page' for Wagtail convention
        'post': post,  # Keep 'post' for backward compatibility
        'recent_posts': recent_posts,
        'categories': all_categories,  # For backward compatibility
        'all_categories': all_categories,
        'post_categories': post_categories,
    })
