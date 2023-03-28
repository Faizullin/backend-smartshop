from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status, permissions,generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SystemData
from .serializers import *
import psutil, time
from shop_app.models import CustomUser

def getStatData(context):
        # cpu_percent = psutil.cpu_percent()


    # mem_percent = psutil.virtual_memory().percent
    # disk_percent = psutil.disk_usage('/').percent
    # timestamp = int(time.time())

    #     # Get CPU times as a named tuple
    # cpu_times = psutil.cpu_times()

    # # Get CPU frequency
    # cpu_freq = psutil.cpu_freq()

    # # Get CPU statistics
    # cpu_stats = psutil.cpu_stats()


    # # Get system load averages
    # load_avg = psutil.getloadavg()

    # # Get disk I/O statistics
    # disk_io_counters = psutil.disk_io_counters()
    
    # # Get currently running processes IDs
    # pids = psutil.pids()
    
    # # Create a new SystemData object and save it to the database
    # # system_data = SystemData(cpu_percent=cpu_percent, mem_percent=mem_percent, disk_percent=disk_percent, timestamp=timestamp)
    # # system_data.save()
    # #system_data = SystemData.objects.all()
    lastSystemData =  SystemData.objects.last()
    user_acts = CustomUser.objects.order_by('-id')[:10]
    context['data']['user_acts'] = {
        'timestamp': [ user.date_joined for user in user_acts ],
        'login': UserSerializer(user_acts, many=True).data,
    }
    context['data']["cpu_times"] = psutil.cpu_times()
    context['data']["cpu_freq"] = psutil.cpu_freq()
    context['data']["cpu_stats"] = psutil.cpu_stats()
    context['data']["load_avg"] = random.randint(20,27) #psutil.getloadavg()
    context['data']["disk_io_counters"] = psutil.disk_io_counters()
    context['data']["net_io_counters"] = psutil.net_io_counters()
    context['data']['system_data'] = SystemDataSerializer(lastSystemData).data
    context['MY_MONITORING'] = True
    return context

@login_required()
def server0(request):
    context = {
        'segment': 'monitoring_server0',
        'data': { }
    }
    context = getStatData(context)
    return render(request, 'dashboard/monitoring/server0-stats.html', context)

@login_required()
def server1(request):
    context = {
        'segment': 'monitoring_server1',
        'data': {},
    }
    context = getStatData(context)
    return render(request, 'dashboard/monitoring/server1-stats.html', context)

class ApiServerData(APIView):
    # authentication_classes = [JWTAuthentication, ]
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        context = {
            'segment': 'monitoring_server1',
            'data': {},
        }
        context = getStatData(context)
        return Response(data = context)
    

started = False
MAX_SAVE_NUMBER = 20
import random
def save_system_data():
    global MAX_SAVE_NUMBER
    global started
    print("Start save_system_data")  
    while True:
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        cpu_temp = float(random.randint(40,60))
        timestamp = int(time.time())
 
        system_data = SystemData(cpu_percent=cpu_percent, mem_percent=mem_percent, disk_percent=disk_percent, timestamp=timestamp, cpu_temp=cpu_temp)
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