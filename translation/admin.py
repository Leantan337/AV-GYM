from django.contrib import admin
from .models import Translation

# Register your models here.

@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('source_text', 'target_language', 'translated_text', 'source_language', 'updated_at')
    list_filter = ('target_language', 'source_language', 'updated_at')
    search_fields = ('source_text', 'translated_text')
    ordering = ('source_language', 'target_language', 'source_text')
    date_hierarchy = 'updated_at'
    fieldsets = (
        (None, {
            'fields': ('source_text', 'translated_text')
        }),
        ('Language Details', {
            'fields': ('source_language', 'target_language')
        }),
    )
