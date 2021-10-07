from django.contrib import admin
from .models import *

# Register your models here.
all_models = [PropertyAccount, CollectionAccount, PlantAccount, Bin, CollectionTask, Property, Scan]
admin.site.register(all_models)