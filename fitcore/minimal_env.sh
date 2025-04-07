#!/bin/bash

# Django settings
export DJANGO_SETTINGS_MODULE=fitcore.settings_production
export DJANGO_SECRET_KEY="django-insecure-temp-key-for-development-only"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"

# Database settings - using SQLite for initial setup
export DB_ENGINE="django.db.backends.sqlite3"
export DB_NAME="db.sqlite3"

# Disable optional services for initial setup
export USE_S3=False
export USE_REDIS=False
export ENABLE_SECURITY=False

# Create required directories
mkdir -p media staticfiles

# Set correct permissions
chmod 755 media staticfiles
