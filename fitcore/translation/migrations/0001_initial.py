# Generated by Django 4.2.20 on 2025-04-08 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_text', models.TextField(verbose_name='Source Text')),
                ('target_language', models.CharField(max_length=10, verbose_name='Target Language')),
                ('translated_text', models.TextField(verbose_name='Translated Text')),
                ('source_language', models.CharField(default='en', max_length=10, verbose_name='Source Language')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Manual Translation',
                'verbose_name_plural': 'Manual Translations',
                'unique_together': {('source_text', 'target_language', 'source_language')},
            },
        ),
    ]
