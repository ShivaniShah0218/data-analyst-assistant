from .tasks import celery_app
# Run using:
# celery -A app.celery_worker.celery_app worker --loglevel=info
