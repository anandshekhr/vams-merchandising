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
from rest_framework import filters,pagination
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class PincodeListCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = PincodeDetail.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pincode']
    serializer_class = PincodeDetailSerializer

class PincodeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = PincodeDetail.objects.all()
    serializer_class = PincodeDetailSerializer