# import asyncio
# import psutil
# import time
# from .models import SystemData

# async def save_system_data():
#     while True:
#         # Get the system data
#         cpu_percent = psutil.cpu_percent()
#         mem_percent = psutil.virtual_memory().percent
#         disk_percent = psutil.disk_usage('/').percent
#         timestamp = int(time.time())

#         # Create a new SystemData object and save it to the database
#         system_data = SystemData(cpu_percent=cpu_percent, mem_percent=mem_percent, disk_percent=disk_percent, timestamp=timestamp)
#         system_data.save()

#         # Wait for 1 second before getting the next set of data
#         await asyncio.sleep(1)

# async def main():
#     # Start the asynchronous task to save system data
#     await save_system_data()

# # Start the event loop to run the asynchronous task
# asyncio.run(main())