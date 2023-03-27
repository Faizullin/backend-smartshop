from django.core.management.base import BaseCommand
from monitoring.models import SystemData
import asyncio
import psutil
import time 

class Command(BaseCommand):
    help = 'Save system data to database'

    def handle(self, *args, **options):
    # Start the asynchronous task to save system data
        asyncio.run(save_system_data())

async def save_system_data():
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

        # Wait for 1 second before getting the next set of data
        await asyncio.sleep(1)

