from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SystemData
import psutil, time


def system_data(request):
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    timestamp = int(time.time())
    cpu_percent = psutil.cpu_percent()

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
        #'system_data': system_data,
    }
    context["cpu_percent"] = cpu_percent
    context["cpu_times"] = cpu_times
    context["cpu_freq"] = cpu_freq
    context["cpu_stats"] = cpu_stats
    context["load_avg"] = load_avg
    context["disk_io_counters"] = disk_io_counters
    context["pids"] = pids
    context['system_data'] = SystemData.objects.last()
    return render(request, 'dashboard/monitoring/server1-stats.html', context)









@login_required()
def server1(*args, **kwargs):
    return system_data(*args, **kwargs) 
