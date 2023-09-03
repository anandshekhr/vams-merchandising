from django.shortcuts import render
from stores.models import FAQ,PoliciesDetails
# Create your views here.
def renderFAQPage(request):
    faq_details_five = FAQ.objects.all()[:5]
    faq_details_last_six = FAQ.objects.all()[5:11]
    context = {'faq_details_five': faq_details_five,
               'faq_details_last_six': faq_details_last_six}

    return render(request,'faq.html',context)

def refund_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies}
    return render(request,'policies/refund_policy.html',context)


def return_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies}
    return render(request, 'policies/return_policy.html', context)


def shipping_and_delivery_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies}
    return render(request, 'policies/shipping_and_delivery_policy.html', context)


def payment_terms_and_conditions_policy(request):
    policies = PoliciesDetails.objects.get()
    context = {'policy': policies}
    return render(request, 'policies/payment_terms_and_conditions_policy.html', context)

