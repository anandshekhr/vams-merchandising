from django.shortcuts import render
from products.models import *
from .models import *
from about.models import VCReview
from django.shortcuts import get_object_or_404


# Create your views here.
def get_meta_data(path_name, domain):
    canonical_path = "https://www." + domain + path_name
    meta_data, _ = MetaDetail.objects.get_or_create(
        page=path_name, canonical=canonical_path
    )
    title = meta_data.meta_title
    key = meta_data.meta_tag
    desc = meta_data.meta_description
    canonical = meta_data.canonical
    return title, desc, key, canonical


def home(request):
    banners = Banners.objects.all()
    products_hc = Products.objects.filter(
        category__in=Categories.objects.filter(category_code="clothing-and-apparel"),
        display_home=True,
    )
    len_hc = len(products_hc)
    products_bs = Products.objects.filter(
        category__in=Categories.objects.filter(category_code="best-seller"),
        display_home=True,
    )
    len_bs = len(products_bs)
    products_tr = Products.objects.filter(
        category__in=Categories.objects.filter(category_code="trending"),
        display_home=True,
    )
    len_tr = len(products_tr)
    products_na = Products.objects.filter(
        category__in=Categories.objects.filter(category_code="new-arrival"),
        display_home=True,
    )
    len_na = len(products_na)

    # metadata

    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "Banners": banners,
        "Products_hc": products_hc,
        "Products_bs": products_bs,
        "Products_tr": products_tr,
        "Products_na": products_na,
        "len_hc": len_hc,
        "len_bs": len_bs,
        "len_tr": len_tr,
        "len_na": len_na,
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "index.html", context)


def err_500(request):
    # metadata

    title, desc, key, canonical = get_meta_data(request.path, request.get_host())
    context = {
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "error/500.html", context)


def aboutUs(request):
    reviews = VCReview.objects.filter(active=True)
    # metadata

    title, desc, key, canonical = get_meta_data(request.path, request.get_host())
    return render(
        request,
        "about/about.html",
        {
            "reviews": reviews,
            "page_title": title,
            "description": desc,
            "keyword": key,
            "canonical": canonical,
        },
    )
