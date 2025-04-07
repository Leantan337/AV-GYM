#!/bin/bash

# Django settings
export DJANGO_SETTINGS_MODULE=fitcore.settings_production
export DJANGO_SECRET_KEY="your-secure-secret-key-here"  # Change this!
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"  # Change in production

# Database settings
export DB_NAME="fitcore_db"
export DB_USER="fitcore_user"
export DB_PASSWORD="your-db-password-here"  # Change this!
export DB_HOST="localhost"
export DB_PORT="5432"

# Redis cache
export REDIS_URL="redis://127.0.0.1:6379/1"

# Email settings
export EMAIL_HOST="smtp.gmail.com"
export EMAIL_PORT="587"
export EMAIL_HOST_USER="your-email@gmail.com"  # Change this!
export EMAIL_HOST_PASSWORD="your-app-password"  # Change this!
export DEFAULT_FROM_EMAIL="your-email@gmail.com"  # Change this!

# AWS S3 settings
export AWS_ACCESS_KEY_ID="your-access-key"  # Change this!
export AWS_SECRET_ACCESS_KEY="your-secret-key"  # Change this!
export AWS_STORAGE_BUCKET_NAME="your-bucket-name"  # Change this!
export AWS_S3_REGION_NAME="us-east-1"
export AWS_S3_CUSTOM_DOMAIN="your-cloudfront-domain.cloudfront.net"  # Optional

# Security settings
export CORS_ORIGIN_WHITELIST="https://example.com,https://www.example.com"

# Error tracking
export SENTRY_DSN="your-sentry-dsn"  # Change this!

# Performance monitoring
export SCOUT_KEY="your-scout-key"  # Optional
