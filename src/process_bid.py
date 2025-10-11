import json
import os
from datetime import datetime
from decimal import Decimal

import boto3
from aws_lambda_powertools import Logger
from aws_xray_sdk.core.lambda_launcher import LambdaContext

from domain import Bid

bids_table_name = os.environ['BIDS_TABLE']
dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table(bids_table_name)
logger = Logger(service="BidService")


def parse_record(record: dict) -> Bid:
    return Bid(**{
        **record,
        "amount": Decimal(record['amount']),
        "time_placed": datetime.fromisoformat(record['time_placed']),
        "time_processed": datetime.now()
    })


def save_bid(bid):
    # Bid should be unique
    if bid.amount < 0:
        raise ValueError("Amount should not be negative")

    item = {
        "PK": f"BID#{bid.id}",
        **bid.to_json()
    }
    bids_table.put_item(Item=item)


@logger.inject_lambda_context
def lambda_handler(event: dict, _context: LambdaContext):
    failed_records = []
    for record in event['Records']:
        body = json.loads(record['body'])
        try:
            logger.debug("Processing record", extra={"record": record})

            bid = parse_record(body)
            save_bid(bid)
            logger.info("Successfully saved bid", extra={"bid": bid})
        except Exception:
            logger.error("Failed processing record", extra={"record": record})
            failed_records.append({
                'itemIdentifier': record['messageId']
            })

    return {"batchItemFailures": failed_records}
