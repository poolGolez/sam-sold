import json
import os
from datetime import datetime
from decimal import Decimal

import boto3
from aws_xray_sdk.core.lambda_launcher import LambdaContext

from domain import Bid

bids_table_name = os.environ['BIDS_TABLE']
dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table(bids_table_name)


#  This is polling shit!y

def lambda_handler(event: dict, context: LambdaContext):
    for record in event['Records']:
        print(">>>>> PROCESSING BID [start] >>>>>")
        print(record)
        print("<<<<< PROCESSING BID [end] <<<<<")

        body = json.loads(record['body'])
        print(body)

        bid = Bid(**{
            **body,
            "amount": Decimal(body['amount']),
            "time_placed": datetime.fromisoformat(body['time_placed']),
            "time_processed": datetime.now()
        })

        print("~~~~~", bid)
        bids_table.put_item(Item=(bid.to_json()))
        print(f"Successfully saved bid {bid.id}")

    return {"status": 200}
