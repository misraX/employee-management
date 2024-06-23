from celery import Celery
from celery.schedules import crontab

from server.employee_management.core.configurations.configuration import configuration

app = Celery(
    "employee_management",
    broker=configuration.celery_broker_url,
    backend=configuration.celery_broker_url,
)
app.conf.update(
    include=["server.employee_management.scheduler.celery.tasks"],
    result_expires=3600,
    beat_schedule={
        "send-employee-holidays-email-every-monday": {
            "task": "server.employee_management.scheduler.celery.tasks.employee_upcoming_holidays",
            "schedule": crontab(minute="0", hour="0", day_of_week="monday"),  # Monday
        },
    },
)
