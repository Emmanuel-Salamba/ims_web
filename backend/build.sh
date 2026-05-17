#!/bin/bash
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input

# Create superuser if it doesn't exist (using environment variables)
python manage.py createsu

echo "Build completed successfully!"