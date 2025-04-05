from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet
from django import forms

# Create your models here.

# Blog index page model
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['blog_entries'] = BlogPage.objects.child_of(self).live().order_by('-date')
        return context

# Blog category snippet model
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

# Blog post page model
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        Image,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    categories = models.ManyToManyField(BlogCategory, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('featured_image'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['recent_posts'] = BlogPage.objects.live().order_by('-date')[:5]
        context['categories'] = BlogCategory.objects.all()
        context['all_categories'] = BlogCategory.objects.all()
        # Add selected categories for this post
        context['post_categories'] = self.categories.all()
        return context

    def get_template(self, request, *args, **kwargs):
        # Use different templates for previews vs. published pages
        # Safely check if request has is_preview attribute
        if hasattr(request, 'is_preview') and request.is_preview:
            return 'blog_detail.html'
        return 'blog-details.html'

    class Meta:
        ordering = ['-date']
