from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SystemData
import psutil, time


def system_data(request):
    lastSystemData =  SystemData.objects.last()

    # Get CPU frequency
    cpu_freq = psutil.cpu_freq()

    # Get CPU statistics
    cpu_stats = psutil.cpu_stats()


    # Get system load averages
    load_avg = psutil.getloadavg()

    # Get disk I/O statistics
    disk_io_counters = psutil.disk_io_counters()
    
    context = {
        'segment': 'monitoring_server1',
        'system_data': system_data,
        'data': {
        
        }
    }
    context['data']["cpu_times"] = psutil.cpu_times()
    context['data']["cpu_freq"] = cpu_freq
    context['data']["cpu_stats"] = cpu_stats
    context['data']["load_avg"] = load_avg
    context['data']["disk_io_counters"] = disk_io_counters
    context['data']["net_io_counters"] = psutil.net_io_counters()
    context['data']['sent'] = psutil.net_io_counters().bytes_sent
    context['data']['received'] = psutil.net_io_counters().bytes_recv
    
    
    context['data']['system_data'] = lastSystemData
    context['data']['cpu_percent'] = lastSystemData.cpu_percent
    return render(request, 'dashboard/monitoring/server1-stats.html', context)

def apiServerData(request):
    cpu_percent = psutil.cpu_percent()


    mem_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    timestamp = int(time.time())

        # Get CPU times as a named tuple
    cpu_times = psutil.cpu_times()

    # Get CPU frequency
    cpu_freq = psutil.cpu_freq()

    # Get CPU statistics
    cpu_stats = psutil.cpu_stats()


    # Get system load averages
    load_avg = psutil.getloadavg()

    # Get disk I/O statistics
    disk_io_counters = psutil.disk_io_counters()
    
    # Get currently running processes IDs
    pids = psutil.pids()
    
    # Create a new SystemData object and save it to the database
    # system_data = SystemData(cpu_percent=cpu_percent, mem_percent=mem_percent, disk_percent=disk_percent, timestamp=timestamp)
    # system_data.save()
    #system_data = SystemData.objects.all()
    context = {
        'segment': 'monitoring_server1',
        'data': {},
    }
    context['data']["cpu_percent"] = cpu_percent
    context['data']["cpu_times"] = cpu_times
    context['data']["cpu_freq"] = cpu_freq
    context['data']["cpu_stats"] = cpu_stats
    context['data']["load_avg"] = load_avg
    context['data']["disk_io_counters"] = disk_io_counters
    context['data']['sent'] = psutil.net_io_counters().bytes_sent
    context['data']['received'] = psutil.net_io_counters().bytes_recv
    context['data']['timestamp'] = psutil.cpu_times().user
    #context['data']['system_data'] = SystemData.objects.last()
    return JsonResponse(data = context)










@login_required()
def server1(*args, **kwargs):
    return system_data(*args, **kwargs) 



started = False
MAX_SAVE_NUMBER = 20
def save_system_data():
    global MAX_SAVE_NUMBER
    global started
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
            first_n_records = SystemData.objects.order_by('id').filter(id__lt = (system_data.pk - MAX_SAVE_NUMBER))
            first_n_records.delete()
            
        time.sleep(7)

from threading import Thread
def apiStartRecord(request):
    global started
    if started:
        return JsonResponse({"data":"Already started!"})
    elif not started:
        started = True
        t1 = Thread(target=save_system_data,daemon=True)
        t1.start()      
        return JsonResponse({"data":"Starting"})