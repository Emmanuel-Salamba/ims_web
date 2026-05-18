#!/bin/bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input

# Create superuser if needed (don't fail build if it fails)
python manage.py createsu || echo "Superuser creation skipped"

echo "Build completed successfully!"