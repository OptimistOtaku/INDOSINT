from celery import Celery
from celery.schedules import crontab
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Create Celery app
celery_app = Celery(
    "indosint",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.osint_tasks",
        "app.tasks.analysis_tasks",
        "app.tasks.ml_tasks",
        "app.tasks.data_processing_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task routing
    task_routes={
        "app.tasks.osint_tasks.*": {"queue": "osint"},
        "app.tasks.analysis_tasks.*": {"queue": "analysis"},
        "app.tasks.ml_tasks.*": {"queue": "ml"},
        "app.tasks.data_processing_tasks.*": {"queue": "data_processing"},
    },
    
    # Task execution
    task_always_eager=False,
    task_eager_propagates=True,
    task_ignore_result=False,
    task_store_errors_even_if_ignored=True,
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Result backend
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Beat schedule
    beat_schedule={
        # Daily OSINT data collection
        "daily-social-media-collection": {
            "task": "app.tasks.osint_tasks.collect_social_media_data",
            "schedule": crontab(hour=2, minute=0),  # 2 AM daily
            "args": (),
        },
        "daily-news-collection": {
            "task": "app.tasks.osint_tasks.collect_news_data",
            "schedule": crontab(hour=3, minute=0),  # 3 AM daily
            "args": (),
        },
        "daily-professional-data-collection": {
            "task": "app.tasks.osint_tasks.collect_professional_data",
            "schedule": crontab(hour=4, minute=0),  # 4 AM daily
            "args": (),
        },
        
        # Hourly analysis tasks
        "hourly-behavioral-analysis": {
            "task": "app.tasks.analysis_tasks.analyze_behavioral_patterns",
            "schedule": crontab(minute=0),  # Every hour
            "args": (),
        },
        "hourly-risk-assessment": {
            "task": "app.tasks.analysis_tasks.assess_risk_scores",
            "schedule": crontab(minute=30),  # Every hour at 30 minutes
            "args": (),
        },
        
        # Weekly tasks
        "weekly-digital-dna-update": {
            "task": "app.tasks.analysis_tasks.update_digital_dna_profiles",
            "schedule": crontab(day_of_week=1, hour=5, minute=0),  # Monday 5 AM
            "args": (),
        },
        "weekly-prediction-model-update": {
            "task": "app.tasks.ml_tasks.update_prediction_models",
            "schedule": crontab(day_of_week=1, hour=6, minute=0),  # Monday 6 AM
            "args": (),
        },
        
        # Data cleanup tasks
        "daily-data-cleanup": {
            "task": "app.tasks.data_processing_tasks.cleanup_old_data",
            "schedule": crontab(hour=1, minute=0),  # 1 AM daily
            "args": (),
        },
        "weekly-data-archival": {
            "task": "app.tasks.data_processing_tasks.archive_old_data",
            "schedule": crontab(day_of_week=0, hour=7, minute=0),  # Sunday 7 AM
            "args": (),
        },
        
        # System maintenance
        "daily-system-health-check": {
            "task": "app.tasks.system_tasks.system_health_check",
            "schedule": crontab(hour=0, minute=0),  # Midnight daily
            "args": (),
        },
        "weekly-performance-optimization": {
            "task": "app.tasks.system_tasks.optimize_performance",
            "schedule": crontab(day_of_week=0, hour=8, minute=0),  # Sunday 8 AM
            "args": (),
        },
    },
    
    # Task execution time limits
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,  # 10 minutes
    
    # Retry configuration
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_remote_tracebacks=True,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Task error handling
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery setup"""
    logger.info(f"Request: {self.request!r}")

# Task failure handling
@celery_app.task_failure.connect
def handle_task_failure(sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, einfo=None, **kw):
    """Handle task failures"""
    logger.error(
        "Task failed",
        task_id=task_id,
        task_name=sender.name if sender else None,
        exception=str(exception),
        args=args,
        kwargs=kwargs
    )

# Task success handling
@celery_app.task_success.connect
def handle_task_success(sender=None, result=None, **kw):
    """Handle task successes"""
    logger.info(
        "Task completed successfully",
        task_name=sender.name if sender else None,
        result=result
    )

# Task retry handling
@celery_app.task_retry.connect
def handle_task_retry(sender=None, request=None, reason=None, einfo=None, **kw):
    """Handle task retries"""
    logger.warning(
        "Task retry",
        task_name=sender.name if sender else None,
        reason=reason,
        retry_count=request.retries if request else 0
    )

if __name__ == "__main__":
    celery_app.start() 