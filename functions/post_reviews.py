#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(dict):
    client = Cloudant.iam(
        account_name = dict["COUCH_USERNAME"],
        api_key = dict["IAM_API_KEY"],
        connect = True,
    )
    
    print(dict)
    
    
    
    my_database = client['reviews']
    
    try:
        my_document = my_database.create_document(dict["review"])
        if my_document.exists():
            result = {
                "message": "Data Inserted Successfully"
            }
        return result
    except:
        return {
            'statusCode': 404,
            'message': "SomethingWent Wrong"
        }