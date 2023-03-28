import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='name')
    year = models.DateField()
    dealer_id = models.IntegerField()
    sedan = 'Sedan'
    suv = 'SUV'
    wagon = 'Wagon'
    coup = 'Coup'
    car_types = [
        (sedan, "Sedan"),
        (suv, "SUV"),
        (wagon, "Wagon"),
        (coup, "Coup")
    ]
    car_type = models.CharField(max_length=5, choices=car_types, default=sedan)

    def __str__(self):
        return "Name: " + self.name


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data


class DealerReview:
    def __init__(self, dealership_name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership_name = dealership_name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
