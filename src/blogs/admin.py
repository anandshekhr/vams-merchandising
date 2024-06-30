from django.contrib import admin
from .models import *
# Register your models here.


class BlogsAdmin(admin.ModelAdmin):
    list_display: list = ('title','author','content','tags',
                          'created_at', 'modified_at')
    ordering: list = ['-modified_at']
    search_fields: list = ('title','author','content','tags')


admin.site.register(Blogs, BlogsAdmin)
