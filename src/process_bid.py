import json
import os
from datetime import datetime
from decimal import Decimal

import boto3
from aws_lambda_powertools import Logger
from aws_xray_sdk.core.lambda_launcher import LambdaContext

from domain import Bid, LotStatus
from dao import find_lot

bids_table_name = os.environ['BIDS_TABLE']
dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table(bids_table_name)
logger = Logger(service="BidService")


def parse_record(record: dict) -> Bid:
    return Bid(**{
        **record,
        "amount": Decimal(str(record['amount'])),
        "time_placed": datetime.fromisoformat(record['time_placed']),
        "time_processed": datetime.now()
    })


def process_bid(bid):
    lot = find_lot(bids_table, bid.lot_id)
    if lot is None:
        raise ValueError(f"Lot {bid.lot_id} does not exists")

    if lot.status != LotStatus.OPEN:
        raise ValueError(f"Lot {lot.id} is currently not OPEN")

    if bid.amount < 0:
        raise ValueError("Amount should not be negative")

    bids_table.put_item(
        Item={
            "PK": f"BID#{bid.id}",
            **bid.to_json()
        },
        ConditionExpression='attribute_not_exists(PK)'
    )

    if lot.highest_bid_id is None or lot.highest_bid_amount < bid.amount:
        bids_table.update_item(
            Key={
                'PK': f"LOT#{lot.id}"  # Replace with your actual key name and value
            },
            UpdateExpression='SET highest_bid_id = :bid_id, highest_bid_amount = :bid_amount',
            ExpressionAttributeValues={
                ":bid_id": bid.id,
                ":bid_amount": bid.amount
            }
        )

        logger.info(f"The bid for LOT {lot.id} has increased to {bid.amount}", extra={"lot": lot, "bid": bid})


@logger.inject_lambda_context
def lambda_handler(event: dict, _context: LambdaContext):
    failed_records = []
    logger.info(f"Processing {len(event['Records'])} records.")
    for record in event['Records']:
        body = json.loads(record['body'])
        try:
            logger.debug("Processing record", extra={"record": record})

            bid = parse_record(body)
            process_bid(bid)
            logger.info("Successfully saved bid", extra={"bid": bid})
        except Exception as error:
            logger.error("Failed processing record", extra={"record": record, "error": error})
            failed_records.append({
                'itemIdentifier': record['messageId']
            })

    return {"batchItemFailures": failed_records}
