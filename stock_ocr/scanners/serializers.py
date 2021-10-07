from rest_framework import serializers
from .models import Scan, Property, Bin, CollectionTask

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
                    'owner',
                    'address',
                    'lat',
                    'lon',
                    )

        
class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = (
                    'bin',
                    'percent_full',
                    'scan_date',
                    )


class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = (
                    'property',
                    'waste_type',
                    'bin_capacity',
                    )

class CollectionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionTask
        fields = (
                    'bin',
                    'destination',
                    'collector',
                    'due_date'
                    )

