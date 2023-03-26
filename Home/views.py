from django.shortcuts import render
from products.models import *

# Create your views here.


def home(request):
    banners = Banners.objects.all()
    products = Products.objects.all()
    product_images = ProductImages.objects.all()
    context = {'Banners': banners, 'Products': products,
               'pr_images': product_images}
    return render(request, 'index.html', context)


def err_500(request):
    return render(request, '500.html')
