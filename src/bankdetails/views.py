from django.shortcuts import render,HttpResponse
import pandas as pd
from .models import *
from datetime import datetime
import os
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .serializer import *
from delivery.models import PincodeDetail


def writeExcelToSQL(request):
    # total = int(total)
    
    # filename= "bankdetails/68774.xlsx"
    # df = pd.read_excel(os.path.join(os.getcwd(),filename))
    # for index,row in df.iterrows():
        
    #     ifsc = ifscCodeDetails(bank=row[0],ifsc=row[1],branch=row[2],address=row[3],contact=row[8],city1=row[4],city2=row[5],state=row[6],std_code=row[7],active=True,created_at=datetime.now(),modified_at=datetime.now(),bank_code=row[1][:4])
    #     ifsc.save()
    filename = "bankdetails/pincodes.csv"
    df = pd.read_csv(os.path.join(os.getcwd(),filename))
    for index,row in df.iterrows():
        pincode = PincodeDetail(pincode=row[1],locality=row[5],city=row[8],state=row[9],can_deliver_here = True if row[3] == 'Delivery' else False)
        pincode.save()

        
            
    return HttpResponse('success')

class IFSCCodeDetails(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = ifscCodeDetails.objects.all()
    serializer_class = ifscCodeDetailsSerilizer
    pagination_class = PageNumberPagination
    

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = ifscCodeDetailsSerilizer(page, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class getIFSC(APIView):
    permission_classes = [AllowAny,]

    def get(self, request,*args, **kwargs):
        account_number = request.data.get('account_number')
        bank_code = request.data.get('bank_code')
        ifsc_code = ifscCodeDetails.objects.filter(bank_code=bank_code,ifsc__icontains=account_number[:4])
        serializer = ifscCodeDetailsSerilizer(ifsc_code, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)






