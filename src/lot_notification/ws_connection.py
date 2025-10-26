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

    query_params = event['queryStringParameters']
    user_id = query_params.get('user-id', None)
    lot_id = query_params.get('lot-id', None)

    if user_id is None:
        logger.error("Missing query param: user-id", extra={'query': query_params})
        return {'statusCode': 400}

    if lot_id is None:
        logger.error("Missing query param: lot-id", extra={'query': query_params})
        return {'statusCode': 400}

    connection_key = f"CONN#{connection_id}"
    items_to_write = [
        {'PK': f"LOT#{lot_id}", 'SK': connection_key, 'connection_id': connection_id},
        {
            'PK': connection_key,
            'SK': connection_key,
            'connection_id': connection_id,
            'user_id': user_id,
            'details': json.dumps(details),
        }
    ]

    with connections_table.batch_writer() as batch:
        for item in items_to_write:
            batch.put_item(Item=item)
    return {"statusCode": 200}
