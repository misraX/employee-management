from celery import Celery
from celery.schedules import crontab

app = Celery(
    "email_notifier", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

app.conf.update(
    result_expires=3600,
    beat_schedule={
        "send-employee-holidays-email-every-monday": {
            "task": "email_notifier.employee_upcoming_holidays",
            "schedule": crontab(minute="0", hour="0", day_of_week="monday"),  # Monday
        },
    },
)
