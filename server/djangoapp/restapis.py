import requests
import json
from statistics import mean
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibmcloudant import CouchDbSessionAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1


def post_request(url, json_payload):
    request = requests.post(url, json=json_payload)
    print("POST from {} ".format(url))

    status_code = request.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(request.text)

    return request


def post_to_couch_db(review_data):
    COUCH_API = os.environ['COUCH_API']
    COUCH_URL = "https://2e67c53b-5815-48ec-ba03-66f5265a042a-bluemix.cloudantnosqldb.appdomain.cloud"

    authenticator = IAMAuthenticator(COUCH_API)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(COUCH_URL)
    data = review_data

    response = service.post_document(
        db='reviews', document=data).get_result()

    return response


def get_sentiment_score(text):
    LU_url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/dd9b0689-4161-464a-9b6f-3b91e3ad6730"
    watson_lu_api_key = os.environ.get('WATSON_LU_API_KEY')
    api_key = watson_lu_api_key[1:-1]

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(LU_url)

    text_to_analyze = text

    response = natural_language_understanding.analyze(
        text=text_to_analyze,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                     limit=2))).get_result()

    scores = []
    for key_words in response['keywords']:
        scores.append(key_words['sentiment']['score'])

    average_score = mean(scores)

    return average_score


def get_request(url, **kwargs):
    print("GET from {} ".format(url))

    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)

    for doc in json_data['docs']:
        keyToFind = 'review'
        if keyToFind in doc.keys():
            doc['sentiment'] = get_sentiment_score(doc['review'])
            # print(doc)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    json_result = get_request(url)
    dealers = json_result.get("docs", [])
    results = []
    for review in dealers:
        dealer_obj = CarDealer(address=review.get("address"),
                               city=review.get("city"),
                               full_name=review.get("full_name"),
                               id=review.get("id"),
                               lat=review.get("lat"),
                               long=review.get("long"),
                               short_name=review.get("short_name"),
                               st=review.get("st"),
                               zip=review.get("zip"))
        results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    api_key = os.environ.get('WATSON_LU_API_KEY')
    dealer_id = dealerId
    json_result = get_request(url, dealerId=dealer_id, LU_api_key=api_key)
    reviews = json_result.get("docs", [])
    results = []
    for review in reviews:
        dealer_obj = DealerReview(dealership_name=review.get("dealership_name"),
                                  purchase=review.get("purchase"),
                                  purchase_date=review.get(
                                      "fulpurchase_datel_name"),
                                  car_make=review.get("car_make"),
                                  car_model=review.get("car_model"),
                                  car_year=review.get("car_year"),
                                  sentiment=review.get("sentiment"),
                                  id=review.get("id"),
                                  review=review.get("review"))
        results.append(dealer_obj)
    return results
