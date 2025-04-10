from django import template
from django.conf import settings
from translation.models import Translation
import requests

register = template.Library()

@register.filter
def translate_text(text, target_language=None):
    """
    Template filter to translate text. If target_language is not provided or invalid,
    returns the original text.
    """
    # Update to include all supported languages
    if not target_language or target_language not in ['en', 'am', 'ti']:
        return text

    # First try to get translation from database
    translation_obj = Translation.objects.filter(
        source_text=text,
        target_language=target_language
    ).first()

    if translation_obj:
        return translation_obj.translated_text

    # If no translation found in database, return original text
    return text
