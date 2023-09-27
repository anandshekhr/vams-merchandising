from django.shortcuts import render
from products.models import *
from about.models import VCReview


# Create your views here.


def home(request):
    banners = Banners.objects.all()
    products_hc = Products.objects.filter(
        category__in=Categories.objects.filter(category_code='hot-collection'),display_home=True)
    len_hc = len(products_hc)
    products_bs = Products.objects.filter(
        category__in=Categories.objects.filter(category_code='best-seller'),display_home=True)
    len_bs = len(products_bs)
    products_tr = Products.objects.filter(
        category__in=Categories.objects.filter(category_code='trending'),display_home=True)
    len_tr = len(products_tr)
    products_na = Products.objects.filter(
        category__in=Categories.objects.filter(category_code='new-arrival'),display_home=True)
    len_na = len(products_na)
    context = {'Banners': banners, 'Products_hc': products_hc,'Products_bs':products_bs,'Products_tr':products_tr,'Products_na':products_na,'len_hc':len_hc,'len_bs':len_bs,'len_tr':len_tr,'len_na':len_na}
    return render(request, 'index.html', context)


def err_500(request):
    return render(request, '500.html')

def aboutUs(request):
    reviews = VCReview.objects.filter(active=True)
    return render(request,'about.html',{'reviews': reviews})
