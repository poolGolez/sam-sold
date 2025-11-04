import json
import os
from datetime import datetime
from decimal import Decimal

import boto3
from aws_lambda_powertools import Logger
from aws_xray_sdk.core.lambda_launcher import LambdaContext

from dao import find_lot
from domain import Bid, LotStatus

bids_table_name = os.environ['BIDS_TABLE']
dynamodb_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table(bids_table_name)
logger = Logger(service="BidService")


def fetch_lot(lot_id):
    lot = find_lot(bids_table, lot_id)
    if lot is None:
        raise ValueError(f"Lot {lot_id} does not exists")
    if lot.status != LotStatus.OPEN:
        raise ValueError(f"Lot {lot.id} is currently not OPEN")
    return lot


def parse_record(record: dict) -> Bid:
    return Bid(
        id=str(record['id']),
        user_id=str(record['userId']),
        lot_id=str(record['lotId']),
        amount=Decimal(str(record['amount'])),
        time_placed=datetime.fromisoformat(record['timePlaced']),
        time_processed=datetime.now()
    )


def map_to_dynamodb_item(item: dict) -> dict:
    return {k: {'S': v} if isinstance(v, str) else {'N': str(v)}
            for k, v in item.items()}


def map_to_save_bid(bid):
    if bid.amount < 0:
        raise ValueError("Amount should not be negative")

    return {
        'Put': {
            'TableName': bids_table_name,
            'Item': map_to_dynamodb_item({
                "PK": f"BID#{bid.id}",
                **bid.to_json()
            }),
            'ConditionExpression': 'attribute_not_exists(PK)'
        }
    }


@logger.inject_lambda_context
def lambda_handler(event: dict, _context: LambdaContext):
    logger.info(f"Processing {len(event['Records'])} records.")

    lot_id = event['Records'][0]['attributes']['MessageGroupId']
    lot = fetch_lot(lot_id)

    failed_records = []
    message_bid_pairs = []
    for record in event['Records']:
        message_id = record['messageId']
        body = json.loads(record['body'])
        try:
            logger.debug("Processing record", extra={"record": record})

            bid = parse_record(body)
            message_bid_pairs.append((message_id, bid))
        except Exception as error:
            logger.error("Failed processing record", extra={"record": record, "error": error})
            failed_records.append({'itemIdentifier': message_id})

    transaction_items = []
    valid_message_bid_pairs = []
    for (message_id, bid) in message_bid_pairs:
        try:
            transaction_items.append(map_to_save_bid(bid))
            valid_message_bid_pairs.append((message_id, bid))
        except Exception as error:
            logger.error("Failed validation for bid", extra={"bid": bid, "error": error})
            failed_records.append({'itemIdentifier': message_id})

    if len(valid_message_bid_pairs) > 0:
        highest_bid = max([bid for _, bid in valid_message_bid_pairs], key=lambda b: b.amount)

        # Update lot with highest bid
        if lot.highest_bid_id is None or lot.highest_bid_amount < highest_bid.amount:
            transaction_items.append({
                'Update': {
                    'TableName': bids_table_name,
                    'Key': map_to_dynamodb_item({"PK": f"LOT#{lot.id}"}),
                    'UpdateExpression': 'SET highest_bid_id = :bid_id, highest_bid_amount = :bid_amount',
                    'ExpressionAttributeValues': map_to_dynamodb_item({
                        ":bid_id": highest_bid.id,
                        ":bid_amount": highest_bid.amount
                    })
                }
            })

            logger.info(f"The bid for LOT {lot.id} has increased to {highest_bid.amount}",
                        extra={"lot": lot, "bid": highest_bid})

    dynamodb_client.transact_write_items(TransactItems=transaction_items)
    logger.info("Successfully saved bids", extra={"transaction_items": transaction_items})

    return {"batchItemFailures": failed_records}
