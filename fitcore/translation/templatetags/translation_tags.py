from django import template
from django.utils.translation import gettext as _
from translation.models import Translation  # Make sure to import the Translation model

register = template.Library()

@register.filter
def translate_text(text, lang=None):
    """
    Translate text based on the provided language.
    Usage: {{ "Text to translate"|translate_text:language_code }}
    """
    # Update supported languages to match your site
    if not lang or lang not in ['en', 'am', 'ti']:
        return text

    # Try to get translation from database
    try:
        translation_obj = Translation.objects.filter(
            source_text=text,
            target_language=lang
        ).first()
        
        if translation_obj:
            return translation_obj.translated_text
    except:
        # If there's any error (like database connection), return original text
        pass
        
    # If no translation found, return original text
    return text
