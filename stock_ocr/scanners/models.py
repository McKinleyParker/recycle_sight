from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator


TRASH = "tr"
PAPER = "pr"
METAL = "mt"
GLASS = "gl"
PLASTIC = "pl"
CARDBOARD = "cd"

waste_choices = [
    (TRASH, "trash"),
    (PAPER, "paper"),
    (METAL, "metal"),
    (GLASS, "glass"),
    (PLASTIC, "plastic"),
    (CARDBOARD, "cardboard"),
    ]

#account of a property managed by JLL
class PropertyAccount(models.Model): 
    owner_name = models.CharField(max_length=200)
    company_id = models.CharField(max_length=100, primary_key=True)
    company_email = models.CharField(max_length=100)

    def __str__(self):
        return self.owner_name;

#personal account of a driver for a waste collection company
class CollectionAccount(models.Model): 
    owner_name = models.CharField(max_length=200)
    company_id = models.CharField(max_length=100, primary_key=True)
    truck_capacity = models.IntegerField(default=1, validators=[MinValueValidator(1)]) #in tons

#company account of a waste recycling plant that can set daily requirements for sorted waste
class PlantAccount(models.Model): 
    owner_name = models.CharField(max_length=200)
    company_id = models.CharField(max_length=100, primary_key=True)
    company_email = models.CharField(max_length=100) 


class Property(models.Model):
    owner = models.ForeignKey(PropertyAccount, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    lat = models.IntegerField(default=0, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    lon = models.IntegerField(default=0, validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __str__(self):
        return self.address;

class Bin(models.Model):
    

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=2, choices=waste_choices, default=TRASH)
    bin_capacity = models.IntegerField(default=1, validators=[MinValueValidator(1)])


class Scan(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    percent_full = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    scan_date = models.DateTimeField(default=timezone.now)


class CollectionTask(models.Model):
    
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    destination = models.ForeignKey(PlantAccount, on_delete=models.CASCADE)
    collector = models.ForeignKey(CollectionAccount, on_delete=models.CASCADE)

    # default_date = timezone.now() + timedelta(days=2)
    due_date = models.DateTimeField(default=timezone.now)
