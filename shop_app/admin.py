from django.contrib import admin

# Register your models here.
from .models import Shop, CustomUser
# Register your models here.

admin.site.register(Shop)
admin.site.register(CustomUser)