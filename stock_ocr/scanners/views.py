from django.shortcuts import render
from django.http import HttpResponse
from .models import Property, Scan, Bin, CollectionTask, CollectionAccount, PlantAccount
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import PropertySerializer, BinSerializer, ScanSerializer, CollectionTaskSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import api_view


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from datetime import timedelta

# Create your views here.
def index(request):
    return HttpResponse("see, still working")


#uses and API view decorator, should all API views have this
class propertyname(APIView):
    def get(self, request, format=None):
        property_names = Property.objects.all()[0].address

        return Response(property_names)

class propertylocation(APIView):
    def get(self, request, format=None):
        property_locations = [Property.objects.all()[0].lat, "and", Property.objects.all()[0].lon]

        return Response(property_locations)


@api_view(['GET', 'POST', 'DELETE'])
def bin_list(request):
    if request.method == 'GET':
        bins = Bin.objects.all()
        
        property = request.query_params.get('property', None)
        if property is not None:
            bins = bins.filter(title__icontains=property)
        
        bins_serializer = BinSerializer(bins, many=True)
        return JsonResponse(bins_serializer.data, safe=False)
        # 'safe=False' for objects serialization



#########################################################
#most important api in the project, pushes collection tasks to the schedule
#####################################################
@api_view(['GET', 'POST', 'DELETE'])
def scan_list(request):

    print(request)
    if request.method == 'GET':
        scans = Scan.objects.all()
        
        scans_serializer = ScanSerializer(scans, many=True)
        return JsonResponse(scans_serializer.data, safe=False)
        # 'safe=False' for objects serialization


    elif request.method == 'POST':
            # scan_data = JSONParser().parse(request)
            scan_data = request.data
            scan_serializer = ScanSerializer(data=scan_data)
            print(scan_data)
            if scan_serializer.is_valid():
                scan_serializer.save()
                percent_full = int(scan_data["percent_full"])
                print("Percent full " + str(percent_full))
                if percent_full > 50: # 50 percent full is a default value, the value should be set by analysis of historical data from each bin as described in our databricks notebook
                    print("it started")
                    collection_collector = CollectionAccount.objects.get(company_id=1234) # add logic about choosing a driver with excess capacity and optimizing their route
                    collection_destination = PlantAccount.objects.get(company_id=5678) # add logic about choosing a nearby destination that matches the trash value and daily capacity
                    collection_bin = Bin.objects.get(id=1)
                    new_collection_task = CollectionTask.objects.create(bin=collection_bin, destination=collection_destination, collector=collection_collector)
                    new_collection_task.due_date = new_collection_task.due_date + timedelta(days=2) #sets default pickup for two days later
                    print("ready to save object")
                    new_collection_task.save()
                return JsonResponse(scan_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(scan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def collection_task_list(request):

    if request.method == 'GET':
        collection_tasks = CollectionTask.objects.all()
        
        collection_task_serializer = CollectionTaskSerializer(collection_tasks, many=True)
        return JsonResponse(collection_task_serializer.data, safe=False)
        # 'safe=False' for objects serialization