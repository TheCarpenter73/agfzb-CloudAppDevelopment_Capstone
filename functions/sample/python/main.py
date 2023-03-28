"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}


# import json
# from cloudant.client import Cloudant
# from cloudant.error import CloudantException
# import requests

# async def main(params):
#     authenticator = IAMAuthenticator(apikey=params['IAM_API_KEY'])
#     cloudant = CloudantV1.new_instance(authenticator=authenticator)

#     cloudant.set_service_url(params['COUCH_URL'])

#     try:
#         response = await cloudant.post_all_docs(db='dealerships', include_docs=True)

#         docs = [row['doc'] for row in response.result['rows']]

#         return {
#             'statusCode': 200,
#             'headers': {'Content-Type': 'application/json'},
#             'body': json.dumps({'docs': docs})
#         }

#     except ApiException as ae:
#         return {
#             'statusCode': 500,
#             'headers': {'Content-Type': 'application/json'},
#             'body': json.dumps({'error': ae.description})
#         }
