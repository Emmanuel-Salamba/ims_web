#!/bin/bash
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations with error handling
python manage.py migrate --no-input || echo "Migrations failed, continuing..."