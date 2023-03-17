from __future__ import absolute_import, unicode_literals
from celery import shared_task
import psutil
#from .models import Activity


@shared_task()
def get_system_temperature():
    temperature = psutil.cpu_count()
    return temperature

@shared_task()
def log_activity(activity_type, user):
    pass
    #activity = Activity(activity_type=activity_type, user=user)
    #activity.save()

# @task()
# def get_activity_statistics():
#     statistics = {}
#     for activity_type in Activity.ACTIVITY_TYPES:
#         count = Activity.objects.filter(activity_type=activity_type).count()
#         statistics[activity_type] = count
#     return statistics