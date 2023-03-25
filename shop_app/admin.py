from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(Shop)
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(ProductType)
