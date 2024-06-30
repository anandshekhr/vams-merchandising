from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(PincodeDetail)
class PincodeDetailAdmin(admin.ModelAdmin):
    list_display = ('pincode','locality','city','state','can_deliver_here')
    search_fields = ('pincode','locality','city','state','can_deliver_here')
    ordering = ('-pincode','-locality','-city','-state','-can_deliver_here')

    

    
