# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from . import views
 

app_name = 'monitoring'

urlpatterns = [

    path('monitoring/server1', views.server1, name='server1'),

]



MAX_SAVE_NUMBER = 200



from threading import Thread
import time, psutil
from monitoring.models import SystemData
started_func = False

def save_system_data():
    global started_func

    global MAX_SAVE_NUMBER
    if started_func:
        return
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
        current_count = SystemData.objects.count()
        
        if current_count > MAX_SAVE_NUMBER:
            #SystemData.objects.order_by('id')[:(current_count - MAX_SAVE_NUMBER)].delete()
            first_n_records = SystemData.objects.order_by('id').filter(id__lt = (system_data.pk - MAX_SAVE_NUMBER))

# Delete the first 10 records
            first_n_records.delete()
            

        # Wait for 1 second before getting the next set of data
        #await asyncio.sleep(1)
        time.sleep(7)


t1 = Thread(target=save_system_data,daemon=True)
t1.start()


