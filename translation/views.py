from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Translation
import json

@login_required
def dashboard(request):
    """Custom Translation Dashboard view - separate from the Wagtail CMS Dashboard"""
    query = request.GET.get('q', '')
    language = request.GET.get('lang', '')
    
    translations = Translation.objects.all().order_by('-updated_at')
    
    if query:
        translations = translations.filter(
            Q(source_text__icontains=query) | 
            Q(translated_text__icontains=query)
        )
    
    if language:
        translations = translations.filter(
            Q(source_language=language) | 
            Q(target_language=language)
        )
    
    paginator = Paginator(translations, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get unique languages for the filter dropdown
    source_languages = Translation.objects.values_list('source_language', flat=True).distinct()
    target_languages = Translation.objects.values_list('target_language', flat=True).distinct()
    languages = set(list(source_languages) + list(target_languages))
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'language': language,
        'languages': languages,
        'total_translations': Translation.objects.count(),
    }
    
    return render(request, 'translation/dashboard.html', context)

@login_required
def add_translation(request):
    """Add a new translation entry"""
    if request.method == 'POST':
        source_text = request.POST.get('source_text')
        translated_text = request.POST.get('translated_text')
        source_language = request.POST.get('source_language', 'en')
        target_language = request.POST.get('target_language')
        
        if not all([source_text, translated_text, target_language]):
            messages.error(request, 'All fields are required.')
            return redirect('translation:add_translation')
        
        # Check for existing translation
        existing = Translation.objects.filter(
            source_text=source_text, 
            target_language=target_language,
            source_language=source_language
        ).first()
        
        if existing:
            messages.warning(request, 'Translation already exists. The existing translation has been updated.')
            existing.translated_text = translated_text
            existing.save()
        else:
            Translation.objects.create(
                source_text=source_text,
                translated_text=translated_text,
                source_language=source_language,
                target_language=target_language
            )
            messages.success(request, 'Translation added successfully.')
        
        return redirect('translation:dashboard')
    
    return render(request, 'translation/add_translation.html')

@login_required
def edit_translation(request, pk):
    """Edit an existing translation entry"""
    translation = get_object_or_404(Translation, pk=pk)
    
    if request.method == 'POST':
        translation.source_text = request.POST.get('source_text')
        translation.translated_text = request.POST.get('translated_text')
        translation.source_language = request.POST.get('source_language', 'en')
        translation.target_language = request.POST.get('target_language')
        
        translation.save()
        messages.success(request, 'Translation updated successfully.')
        return redirect('translation:dashboard')
    
    context = {
        'translation': translation
    }
    
    return render(request, 'translation/edit_translation.html', context)

@login_required
def delete_translation(request, pk):
    """Delete a translation entry"""
    translation = get_object_or_404(Translation, pk=pk)
    
    if request.method == 'POST':
        translation.delete()
        messages.success(request, 'Translation deleted successfully.')
        return redirect('translation:dashboard')
    
    context = {
        'translation': translation
    }
    
    return render(request, 'translation/delete_translation.html', context)

@require_POST
def translate_text(request):
    """API endpoint for translating text via AJAX"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        target_language = data.get('target_language', '')
        source_language = data.get('source_language', 'en')
        
        if not text or not target_language:
            return JsonResponse({'error': 'Text and target language are required'}, status=400)
        
        # Find translation in database
        translation = Translation.objects.filter(
            source_text=text, 
            target_language=target_language,
            source_language=source_language
        ).first()
        
        if translation:
            return JsonResponse({
                'translated_text': translation.translated_text,
                'source': 'dictionary'
            })
        
        # If not found, return original text
        return JsonResponse({
            'translated_text': text,
            'source': 'original'
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
