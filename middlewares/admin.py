from django.contrib import admin
from .models import *

@admin.register(RequestDataLog)
class RequestDataLogAdmin(admin.ModelAdmin):
    list_display = ('method','path','timestamp')
    

    
