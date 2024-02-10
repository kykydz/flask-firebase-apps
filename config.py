import os

# Get environment variables
IGLOO_BASE_URL = os.getenv('IGLOO_BASE_URL') or 'http://localhost:80'
IGLOO_USER = os.getenv('IGLOO_USER') or 'default'
IGLOO_PASSWORD = os.getenv('IGLOO_PASSWORD') or 'default'