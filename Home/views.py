from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'index.html')


def err_500(request):
    return render(request, '500.html')
