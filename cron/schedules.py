from celery.schedules import crontab

schedule_map = {
    # CORE CONTROLLERS
    "one_minute_tasks": {
        'task': 'cron.tasks.one_minute_tasks',
        'schedule': crontab(minute='*'), 
    },
    "five_minute_tasks": {
        'task': 'cron.tasks.five_minute_tasks',
        'schedule': crontab(minute='*/5'),
    },
    "ten_minute_tasks": {
        'task': 'cron.tasks.ten_minute_tasks',
        'schedule': crontab(minute='*/10'), 
    },
    "30_minute_tasks": {
        'task': 'cron.tasks.thirty_minute_tasks',
        'schedule': crontab(minute='*/30'), 
    },
    "one_hour_tasks": {
        'task': 'cron.tasks.one_hour_tasks',
        'schedule': crontab(minute=0, hour='*'), 
    },
    "one_day_tasks": {
        'task': 'cron.tasks.one_day_tasks',
        'schedule': crontab(minute=0, hour=0), 
    },
    "one_month_tasks": {
        'task': 'cron.tasks.one_month_tasks',
        'schedule': crontab(minute=0, hour=0, day_of_month=1), 
    },
    "one_year_tasks": {
        'task': 'cron.tasks.one_year_tasks',
        'schedule': crontab(minute=0, hour=0, day_of_month=1, month_of_year=1), 
    },
}