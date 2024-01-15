import json
import boto3
import logging
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logger.info("Event json %s" % json.dumps(event))
    logger.info("Context %s" % context)
    
    http_res = {}
    http_res['headers'] = {}
    http_res['headers']['Content-Type'] = 'application/json'
    
    try:
        client = boto3.resource('dynamodb')
        table = client.Table('articles')
        
        title = event['queryStringParameters']['title']

        logger.info("Getting Title Filter %s" % title)
    except KeyError as e:
        logger.info(f'Exception : {str(e)}')
        logger.info(f'Returning 400 error')
        http_res['statusCode'] = 400
        http_res['body'] = json.dumps(f'Got Key Error: {str(e)}')
        return http_res
    
    if not title:
        logger.info("Title is empty")
        response = table.scan()
    else:
        logger.info("Title is not empty")
        
    response = table.scan(
                     FilterExpression = Attr('title').begins_with(title)
                     )
        

    http_res['statusCode'] = 200
    http_res['body'] = json.dumps(response['Items'])
    
    return http_res