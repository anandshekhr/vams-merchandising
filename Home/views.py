from django.shortcuts import render
from products.models import *

# Create your views here.


def home(request):
    banners = Banners.objects.all()
    products_hc = Products.objects.filter(
        category__contains=['hot-collection'],display_home=True)
    len_hc = len(products_hc)
    products_bs = Products.objects.filter(
        category__contains=['best-seller'],display_home=True)
    len_bs = len(products_bs)
    products_tr = Products.objects.filter(
        category__contains=['trending'],display_home=True)
    len_tr = len(products_tr)
    products_na = Products.objects.filter(
        category__contains=['new-arrival'],display_home=True)
    len_na = len(products_na)
    product_images = ProductImages.objects.all()
    context = {'Banners': banners, 'Products_hc': products_hc,'Products_bs':products_bs,'Products_tr':products_tr,'Products_na':products_na,'len_hc':len_hc,'len_bs':len_bs,'len_tr':len_tr,'len_na':len_na,
               'pr_images': product_images}
    return render(request, 'index.html', context)


def err_500(request):
    return render(request, '500.html')

def aboutUs(request):
    return render(request,'about.html')
