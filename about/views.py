from django.shortcuts import render
from stores.models import FAQ,PoliciesDetails
# Create your views here.
def renderFAQPage(request):
    total_count = len(FAQ.objects.all())
    len_first = round(total_count/2)
    faq_details_five = FAQ.objects.all()[:len_first]
    faq_details_last_six = FAQ.objects.all()[len_first:len_first+1]
    context = {'faq_details_five': faq_details_five,
               'faq_details_last_six': faq_details_last_six}

    return render(request,'policies/faq.html',context)

def refund_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies.refund_policy,'name':'Refund Policy'}
    return render(request,'policies/policy.html',context)


def return_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies.return_policy,'name':'Return Policy'}
    return render(request, 'policies/policy.html', context)

def privacy_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies.privacy_policy,'name':'Privacy Policy'}
    return render(request, 'policies/policy.html', context)


def shipping_and_delivery_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies.shipping_and_delivery_policy,'name':'Shipping Policy'}
    return render(request, 'policies/policy.html', context)

def terms_of_service_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies.terms_of_use,'name':'Terms of Use'}
    return render(request, 'policies/policy.html', context)


def payment_terms_and_conditions_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies.payment_type,'name':'Payment Terms and Conditions Policy'}
    return render(request, 'policies/policy.html', context)

