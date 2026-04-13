release: ./release.sh

web: gunicorn config.wsgi --log-file - --log-level debug
celery: celery -A config worker --beat --scheduler django --loglevel=info --concurrency 1
