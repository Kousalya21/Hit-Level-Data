import sys
import json

from script import KeywordRevenueFinder

finder = KeywordRevenueFinder()

def lambda_handler(event, context):
    response = finder.revenue_finder(event['file_name'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
