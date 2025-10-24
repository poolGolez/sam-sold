import json
import os

import boto3
from aws_lambda_powertools import Logger

connections_table_name = os.environ['CONNECTIONS_TABLE']
dynamodb = boto3.resource('dynamodb')
connections_table = dynamodb.Table(connections_table_name)

logger = Logger(service='ConnectionService')


@logger.inject_lambda_context
def lambda_handler(event, _context):
    logger.info("Received event:", extra={'event': event})

    details = event['requestContext']
    connection_id = details['connectionId']
    user_id = event['queryStringParameters']['user']

    connections_table.put_item(Item={
        'PK': connection_id,
        'details': json.dumps(details),
        'user_id': user_id
    })

    return {"statusCode": 200}
