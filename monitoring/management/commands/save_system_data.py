from django.core.management.base import BaseCommand
from monitoring.models import SystemData
import asyncio
import psutil
import time 
from threading import Thread

class Command(BaseCommand):
    help = 'Save system data to database'

    def handle(self, *args, **options):
    # Start the asynchronous task to save system data
        #
        print("Start save_system_data")
        t1 = Thread(target=save_system_data,daemon=True)
        t1.start()
        # while True:
        #     # Get the system data
        #     cpu_percent = psutil.cpu_percent()
        #     mem_percent = psutil.virtual_memory().percent
        #     disk_percent = psutil.disk_usage('/').percent
        #     timestamp = int(time.time())
        #     system_data = SystemData(cpu_percent=cpu_percent, mem_percent=mem_percent, disk_percent=disk_percent, timestamp=timestamp)
        #     system_data.save()


def save_system_data():
    print("Start save_system_data")
    while True:
        # Get the system data
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        timestamp = int(time.time())
 
        # Create a new SystemData object and save it to the database
        system_data = SystemData(cpu_percent=cpu_percent, mem_percent=mem_percent, disk_percent=disk_percent, timestamp=timestamp)
        system_data.save()
        #current_count = SystemData.objects.count()
        #MAX_SAVE_NUMBER = 10
        # if current_count > MAX_SAVE_NUMBER:
        #     SystemData.objects.filter(id__lt = current_count - MAX_SAVE_NUMBER).delete()

        # Wait for 1 second before getting the next set of data
        #await asyncio.sleep(1)
        time.sleep(3)

