import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'}, 
                                    params=params, auth=HTTPBasicAuth('apikey',  kwargs["api_key"]))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
            
    return results


# Get dealer by state
def get_dealer_by_state_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,state=state)
        
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"]
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
           
    return results


# Get dealer by dealerId
def get_dealer_by_id(url, dealerId):
    result = {}
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealerId)
        
    if json_result:
        # Get the row list in JSON as dealers
        result = json_result["data"]
        
    return result



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    
    if json_result:
        # Get the row list in JSON as dealers
        dealerReviews = json_result["data"]
        # For each dealer object
        for review in dealerReviews:
            # Get its content in `doc` object
            review_doc = review


            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"],purchase=review_doc["purchase"],
                        review=review_doc["review"],purchase_date=review_doc["purchase_date"],car_make=review_doc["car_make"],
                        car_model=review_doc["car_model"],car_year=review_doc["car_year"],sentiment="")
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)
            
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
# def analyze_review_sentiments_notworking(text):

#     url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e55d883e-80bf-4349-8a69-0c359736577f" 
#     api_key = "M8GHGDRHBChbRm6onwWS5f0Ixe3axf2lCVyaD-EGpvlT" 
#     version = "2020-08-01" 
#     feature = "sentiment" 
#     return_analyzed_text = True 

#     result_json = get_request(url, text=text, api_key=api_key, version=version, features=feature, 
#                                 return_analyzed_text=return_analyzed_text)

#     return result_json


def analyze_review_sentiments(text): 

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e55d883e-80bf-4349-8a69-0c359736577f" 
    api_key = "M8GHGDRHBChbRm6onwWS5f0Ixe3axf2lCVyaD-EGpvlT" 
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    try:
        response = natural_language_understanding.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
        label=json.dumps(response, indent=2) 
        label = response['sentiment']['document']['label'] 
    except:
        label = "neutral" 
    
    return(label) 

