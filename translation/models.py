from django.db import models

# Create your models here.

class Translation(models.Model):
    source_text = models.TextField(verbose_name="Source Text")
    target_language = models.CharField(max_length=10, verbose_name="Target Language")
    translated_text = models.TextField(verbose_name="Translated Text")
    source_language = models.CharField(max_length=10, default="en", verbose_name="Source Language")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Manual Translation"
        verbose_name_plural = "Manual Translations"
        unique_together = ('source_text', 'target_language', 'source_language')
        
    def __str__(self):
        return f"{self.source_text[:30]}... -> {self.translated_text[:30]}... ({self.target_language})"
