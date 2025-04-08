from django.utils.deprecation import MiddlewareMixin
from django.utils import translation

class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware that sets the language based on URL parameter
    """
    def process_request(self, request):
        language = request.GET.get('lang', None)
        if language:
            if language in ['en', 'es']:  # Only allow supported languages
                translation.activate(language)
                request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = request.GET.get('lang', None)
        if language and language in ['en', 'es']:
            response['Content-Language'] = language
        return response
