from django.shortcuts import render
from stores.models import FAQ, PoliciesDetails
from Home.views import get_meta_data


# Create your views here.
def renderFAQPage(request):
    total_count = len(FAQ.objects.all())
    len_first = round(total_count / 2)
    faq_details_five = FAQ.objects.all()[:len_first]
    faq_details_last_six = FAQ.objects.all()[len_first : len_first + 1]
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "faq_details_five": faq_details_five,
        "faq_details_last_six": faq_details_last_six,
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }

    return render(request, "policies/faq.html", context)


def refund_policy(request):
    policies = PoliciesDetails.objects.get()
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "policy": policies.refund_policy,
        "name": "Refund Policy",
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "policies/policy.html", context)


def return_policy(request):
    policies = PoliciesDetails.objects.get()
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "policy": policies.return_policy,
        "name": "Return Policy",
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "policies/policy.html", context)


def privacy_policy(request):
    policies = PoliciesDetails.objects.get()
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "policy": policies.privacy_policy,
        "name": "Privacy Policy",
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "policies/policy.html", context)


def shipping_and_delivery_policy(request):
    policies = PoliciesDetails.objects.get()
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "policy": policies.shipping_and_delivery_policy,
        "name": "Shipping Policy",
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "policies/policy.html", context)


def terms_of_service_policy(request):
    policies = PoliciesDetails.objects.get()
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "policy": policies.terms_of_use,
        "name": "Terms of Use",
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "policies/policy.html", context)


def payment_terms_and_conditions_policy(request):
    policies = PoliciesDetails.objects.get()
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "policy": policies.payment_type,
        "name": "Payment Terms and Conditions Policy",
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "policies/policy.html", context)
