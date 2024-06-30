from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Notification)
@admin.register(MetaDetail)
class MetaDetailAdmin(admin.ModelAdmin):
    list_display = ('page','meta_title')
    search_fields = ('page','meta_title')
    
