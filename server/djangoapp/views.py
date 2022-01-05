from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_state_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .models import CarModel
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))


        print(user_exist)
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # <HINT> Login the user and 
            login(request, user)
            
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    dealers = []
    if request.method == "GET":
        url = "https://32204ac1.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        context["dealerships"] = dealerships
        
        return render(request, 'djangoapp/index.html', context)

# get dealer by state view
def get_dealer_by_state(request,state):
    context = {}
    dealers = []
    if request.method == "GET":

        url = "https://32204ac1.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerByState = get_dealer_by_state_cf(url, state)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

        for dealer in dealerByState:
            dealers.append(dealer.getAllData)
        # Return a list of dealer short name
        context["dealerByState"] = dealers
      
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealerId):
    context = {}
    dealers = []
    if request.method == "GET":

        url = "https://32204ac1.us-south.apigw.appdomain.cloud/api/reviews"
        # Get dealers from the URL
        dealerById = get_dealer_reviews_from_cf(url, dealerId)
             
        context["dealerReviewById"] = dealerById
        context["dealerId"] = dealerId
      
        return render(request, 'djangoapp/dealer_details.html', context)

    else:
        if request.method == "POST":
            add_review(request, dealerId)
            return render(request, 'djangoapp/index.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealerId):
    if request.method == "GET":
        context = {}

        cars = CarModel.objects.filter(dealerId = dealerId)
        context['cars'] = cars
        context['dealerId'] = dealerId
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == "POST":

        if request.user.is_authenticated:
            
            
            url = "https://32204ac1.us-south.apigw.appdomain.cloud/api/reviews"

            review = {}
            json_payload = {}
            
            review["dealership"] = dealerId
            review["review"] = request.POST['content']
            review["name"] = request.POST.get('name', "n/a")
            review["purchase"] = request.POST.get('purchase', False)
            review["purchase_date"] = datetime.utcnow().isoformat()
            review["car_make"] = request.POST.get('car_make', "n/a")
            review["car_model"] = request.POST.get('car_model', "n/a")
            review["car_year"] = request.POST.get('car_year', "n/a")

            json_payload["review"] = review

            response = post_request(url, json_payload, dealerId=dealerId)
            return redirect("djangoapp:get_dealer_details", dealerId=dealerId)