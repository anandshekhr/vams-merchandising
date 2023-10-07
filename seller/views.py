from django.shortcuts import render,HttpResponse
import pandas as pd
from .models import *
from datetime import datetime
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializer import *
from django.shortcuts import get_object_or_404


# Create your views here.
class SellerListCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class SellerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
        
class SellerStoreDetailsListCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = SellerStoreDetails.objects.all()
    serializer_class = SellerStoreDetailsSerializer

class SellerStoreDetailsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = SellerStoreDetails.objects.all()
    serializer_class = SellerStoreDetailsSerializer
