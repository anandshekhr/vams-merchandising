from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ifscCodeDetails)
class ifscCodeDetailAdmin(admin.ModelAdmin):
    list_display: list = ('bank','ifsc','micr','branch','city1','state')
    search_fields: list = ('bank','branch','micr','ifsc','state','city1')
    ordering: list = ['-bank','-ifsc','-branch','-micr','-state','-city1']
    
