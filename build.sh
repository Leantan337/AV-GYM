#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python fitcore/manage.py collectstatic --no-input --settings=fitcore.settings_production

# Apply any outstanding database migrations
python fitcore/manage.py migrate --settings=fitcore.settings_production
