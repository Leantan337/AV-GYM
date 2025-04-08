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
    if not target_language or target_language not in ['en', 'es']:
        return text

    # First try to get translation from database
    translation_obj = Translation.objects.filter(
        source_text=text,
        target_language=target_language
    ).first()

    if translation_obj:
        return translation_obj.translated_text

    # If no translation in database and LibreTranslate is configured, try API
    if hasattr(settings, 'LIBRETRANSLATE_API_URL'):
        try:
            payload = {
                "q": text,
                "source": "en",
                "target": target_language,
            }
            
            if hasattr(settings, 'LIBRETRANSLATE_API_KEY'):
                payload["api_key"] = settings.LIBRETRANSLATE_API_KEY

            response = requests.post(
                settings.LIBRETRANSLATE_API_URL,
                json=payload
            )
            
            if response.status_code == 200:
                translated = response.json().get('translatedText')
                # Save to database for future use
                Translation.objects.create(
                    source_text=text,
                    target_language=target_language,
                    translated_text=translated
                )
                return translated
        except:
            pass

    # Return original text if translation fails
    return text
