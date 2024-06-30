from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('write-to-xls',writeExcelToSQL,name='write-to-xls'),
    path('ifsc-code',IFSCCodeDetails.as_view(),name='ifsc-code'),
    path('get-ifsc-code',getIFSC.as_view(),name='get-ifsc-code'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)

