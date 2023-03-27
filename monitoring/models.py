from django.db import models

class SystemData(models.Model):
    cpu_percent = models.FloatField()
    mem_percent = models.FloatField()
    disk_percent = models.FloatField()
    timestamp = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CPU: {self.cpu_percent}%, Memory: {self.mem_percent}%, Disk: {self.disk_percent}%, Timestamp: {self.timestamp}"