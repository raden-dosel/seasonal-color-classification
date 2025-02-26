from celery import Celery

# Define the Celery application
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# Configuration options
celery_app.conf.update(
    result_expires=3600,  # Task results will expire in 1 hour
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],  # Ignore other content
    timezone='UTC',
    enable_utc=True,
)

if __name__ == "__main__":
    celery_app.start()
