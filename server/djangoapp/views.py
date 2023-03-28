from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_to_couch_db
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import pprint
from djangoapp.models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


def home(request):
    context = {'title': 'Home'}
    if request.method == "GET":
        if request.user.is_authenticated:
            context['username'] = request.user.username
        return render(request, 'static/index.html', context)


def about(request):
    context = {'title': 'About Us'}
    if request.method == "GET":
        if request.user.is_authenticated:
            context['username'] = request.user.username
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {'title': 'Contact Us'}
    if request.method == "GET":
        if request.user.is_authenticated:
            context['username'] = request.user.username
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

    context = {'title': 'Login',
               'username': username,
               'password': password,
               }

    if request.method == "GET":
        return render(request, 'djangoapp/home.html', context)


def logout_request(request):
    logout(request)
    return redirect("./home")


def registration_request(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            uername = form.clean_data.get('username')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            messages.success(request, f"Account created for {user}!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})


def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/ccf4e8da-03ee-4e2d-ba9d-7c3216a2b676/dealership-package/get-dealerships"
        dealerships = get_dealers_from_cf(url)
        context = {
            'dealership': dealerships
        }
        if request.method == "GET":
            if request.user.is_authenticated:
                context['username'] = request.user.username
            return render(request, 'djangoapp/dealerships.html', context)


def get_review_by_dearship_id(request):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/ccf4e8da-03ee-4e2d-ba9d-7c3216a2b676/api/review"
    id_str = request.GET.get('id')
    id = int(id_str) if id_str.isdigit() else None
    reviews = get_dealer_reviews_from_cf(url, id)

    get_dealerships_url = "https://us-south.functions.appdomain.cloud/api/v1/web/ccf4e8da-03ee-4e2d-ba9d-7c3216a2b676/dealership-package/get-dealerships"
    dealerships = get_dealers_from_cf(get_dealerships_url)

    current_dealership = ''

    for dealership in dealerships:
        if dealership.id == id:
            current_dealership = dealership.full_name

    context = {
        'reviews': reviews,
        'dealer_id': id,
        'dealerships': dealerships,
        'current_dealership': current_dealership
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'djangoapp/dealer_reviews.html', context)


def add_review(request):
    if request.method == 'POST':
        post_response = request.POST
        review_object = {
            'content': post_response['content'],
            'purchasecheck': post_response['purchasecheck'],
            'car': post_response['car'],
            'purchasedate': post_response['purchasedate'],
        }
        print('review_object - ', review_object)
        context = post_to_couch_db(review_object)
        return render(request, 'djangoapp/add_review.html',)

    if request.method == 'GET':
        currrent_dealership = request.GET.get('current_dealership')
        cars = CarModel.objects.all()
        context = {
            'cars': cars,
            'currrent_dealership': currrent_dealership
        }
        if request.user.is_authenticated:
            context['username'] = request.user.username

        return render(request, 'djangoapp/add_review.html', context)


def get_dealership_by_id(request):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/ccf4e8da-03ee-4e2d-ba9d-7c3216a2b676/api/review"
    id = request.GET.get('id')
    dealer = get_dealer_reviews_from_cf(url, id)
    id = request.GET.get('id')
    print(id)
    context = {
        'id': id
    }
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return render(request, 'djangoapp/dealer_details.html', context)
