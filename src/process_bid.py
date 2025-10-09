import json
import os
from datetime import datetime
from decimal import Decimal

import boto3
from aws_xray_sdk.core.lambda_launcher import LambdaContext


def lambda_handler(event: dict, context: LambdaContext):
    for record in event['Records']:
        print(">>>>> PROCESSING BID [start] >>>>>")
        print(record)
        print("<<<<< PROCESSING BID [end] <<<<<")

        body = json.loads(record['body'])
        print(body)
        bid = {
            'id': body['id'],
            'user_id': body['user_id'],
            'lot_id': body['lot_id'],
            'amount': Decimal(body['amount']),
            'time_placed': body['timestamp'],
            'time_processed': datetime.now().isoformat()
        }
        print("~~~~~", bid)
        bids_table.put_item(Item=bid)
        print(f"Successfully saved bid {bid['id']}")

    return {"status": 200}
