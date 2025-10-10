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

def parse_record(record: dict) -> Bid:
    return Bid(**{
        **record,
        "amount": Decimal(record['amount']),
        "time_placed": datetime.fromisoformat(record['time_placed']),
        "time_processed": datetime.now()
    })


def lambda_handler(event: dict, context: LambdaContext):
    for record in event['Records']:
        print(">>>>> PROCESSING BID [start] >>>>>")
        print(record)
        print("<<<<< PROCESSING BID [end] <<<<<")

        bid = parse_record(json.loads(record['body']))
        print("~~~~~", bid)
        bids_table.put_item(Item=(bid.to_json()))
        print(f"Successfully saved bid {bid.id}")

    # TODO: Return unprocessed bids
    return {"status": 200}
