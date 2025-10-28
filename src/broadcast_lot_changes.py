import json
import os
from datetime import datetime
from decimal import Decimal

import boto3
from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from domain import Lot
from domain import LotStatus

connections_table_name = os.environ['CONNECTIONS_TABLE']
websocket_endpoint = os.environ['WEBSOCKET_API_INVOKE_URL']

logger = Logger(service="BroadcastLotChangesService")
dynamodb = boto3.resource('dynamodb')
connections_table = dynamodb.Table(connections_table_name)
apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=websocket_endpoint)


def parse_lot(record: dict) -> Lot:
    return Lot(
        id=(record.get('id').get('S', None)),
        name=(record.get('name').get('S', None)),
        status=(LotStatus[record.get('status').get('S', None)]),
        highest_bid_id=(record.get('highest_bid_id').get('S', None)),
        highest_bid_amount=(Decimal(str(record.get('highest_bid_amount').get('N', None)))),
        time_opened=(datetime.fromisoformat(record.get('time_opened').get('S', None))
                     if record.get('time_opened') is not None else None),
        time_closed=(datetime.fromisoformat(record.get('time_closed').get('S', None))
                     if record.get('time_closed') is not None else None)
    )


def fetch_subscriber_connections(lot):
    return connections_table.query(
        KeyConditionExpression=Key('PK').eq(f"LOT#{lot.id}")
    ).get("Items", [])


def delete_connection(connection):
    connection_key = connection.get('SK')
    lot_key = connection.get('PK')
    items_to_delete = [
        {'PK': connection_key, 'SK': connection_key},
        {'PK': lot_key, 'SK': connection_key},
    ]

    with connections_table.batch_writer() as batch:
        for key in items_to_delete:
            batch.delete_item(Key=key)


@logger.inject_lambda_context
def lambda_handler(event, _context):
    record = event['Records'][0]
    lot = parse_lot(record['dynamodb'].get('NewImage', {}))
    message = json.dumps({'lot': lot.to_json()})

    for connection in fetch_subscriber_connections(lot):
        connection_id = connection.get('connection_id')
        try:
            apigateway.post_to_connection(
                Data=message.encode('utf-8'),
                ConnectionId=connection_id
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'GoneException':
                logger.debug("Deleting stale connection", extra={'connection': connection})
                delete_connection(connection)
            else:
                logger.error(f"Failed to send to {connection_id}: {e}")

    return {"statusCode": 200}
