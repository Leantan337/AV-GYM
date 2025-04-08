from django import template
from django.utils.safestring import mark_safe
from translation.models import Translation

register = template.Library()

@register.filter
def translate_text(text, target_language=None):
    """
    Template filter to translate text to a specified language
    Usage: {{ "Hello World"|translate_text:"es" }}
    Or with request param: {{ "Hello World"|translate_text:request.GET.lang }}
    """
    if not text:
        return text
    
    # If no target language is provided or it's English, return original text
    if not target_language or target_language == 'en':
        return text
    
    # Look for translation in database
    translation_obj = Translation.objects.filter(
        source_text=text,
        target_language=target_language
    ).first()
    
    if translation_obj:
        return translation_obj.translated_text
    
    # Return original text if no translation found
    return text

@register.inclusion_tag('translation/translate_button.html')
def translate_button(source_language='en', target_language='es', button_text='Translate', position='top-right'):
    """
    Template tag to include the translate button on a page
    Usage: {% translate_button source_language='en' target_language='es' %}
    """
    return {
        'source_language': source_language,
        'target_language': target_language,
        'button_text': button_text,
        'position': position
    }

@register.simple_tag(takes_context=True)
def current_language(context):
    """
    Simple tag to get the current language from the request
    Usage: {% current_language %}
    """
    request = context.get('request')
    if request and hasattr(request, 'LANGUAGE_CODE'):
        return request.LANGUAGE_CODE
    return 'en'
