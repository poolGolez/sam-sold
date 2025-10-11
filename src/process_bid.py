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


def parse_record(record: dict) -> Bid:
    return Bid(**{
        **record,
        "amount": Decimal(record['amount']),
        "time_placed": datetime.fromisoformat(record['time_placed']),
        "time_processed": datetime.now()
    })


def save_bid(bid):
    if bid.amount < 0:
        raise ValueError("Amount should not be negative")

    item = {
        "PK": f"BID#{bid.id}",
        **bid.to_json()
    }
    bids_table.put_item(Item=item)


def lambda_handler(event: dict, context: LambdaContext):
    failed_records = []
    for record in event['Records']:
        body = json.loads(record['body'])
        try:
            print(f"Processing record {record}")

            bid = parse_record(body)
            save_bid(bid)
            print(f"Successfully saved bid {bid.id}")
        except Exception:
            print(f"Failed processing bid {body['id']}")
            failed_records.append({
                'itemIdentifier': record['messageId']
            })

    return {"batchItemFailures": failed_records}
