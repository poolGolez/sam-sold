import json
import os
from datetime import datetime
from decimal import Decimal
from typing import Optional

import boto3
from aws_lambda_powertools import Logger
from aws_xray_sdk.core.lambda_launcher import LambdaContext

from domain import Bid, Lot, LotStatus

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


def save_bid(bid):
    lot = find_lot(bid.lot_id)
    if lot is None:
        raise ValueError(f"Lot {bid.lot_id} does not exists")

    # Lot should be ACTIVE!

    if bid.amount < 0:
        raise ValueError("Amount should not be negative")

    bids_table.put_item(
        Item={
            "PK": f"BID#{bid.id}",
            **bid.to_json()
        },
        ConditionExpression='attribute_not_exists(PK)'
    )


def find_lot(lot_id: str) -> Optional[Lot]:
    response = bids_table.get_item(
        Key={"PK": f"LOT#{lot_id}"},
        ConsistentRead=True,
    )

    item = response.get('Item')
    if item is None:
        return None

    lot = Lot(
        id=item['id'],
        name=item['name'],
        status=LotStatus[item['status']],
        highest_bid_id=item.get('highest_bid_id'),
        highest_bid_amount=item.get('highest_bid_amount'),
        time_opened=datetime.fromisoformat(item['time_opened']) if item.get('time_opened') is not None else None,
        time_closed=datetime.fromisoformat(item['time_closed']) if item.get('time_closed') is not None else None
    )

    return lot


@logger.inject_lambda_context
def lambda_handler(event: dict, _context: LambdaContext):
    failed_records = []
    logger.info(f"Processing {len(event['Records'])} records.")
    for record in event['Records']:
        body = json.loads(record['body'])
        try:
            logger.debug("Processing record", extra={"record": record})

            bid = parse_record(body)
            save_bid(bid)
            logger.info("Successfully saved bid", extra={"bid": bid})
        except Exception as error:
            logger.error("Failed processing record", extra={"record": record, "error": error})
            failed_records.append({
                'itemIdentifier': record['messageId']
            })

    return {"batchItemFailures": failed_records}
