import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from dao import find_lot, find_all_lots

app = APIGatewayRestResolver()
logger = Logger(service="Lot API")
bids_table_name = os.environ['BIDS_TABLE']
dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table(bids_table_name)


@app.get("/lots")
def get_lot():
    lots = find_all_lots(bids_table)
    return {
        "data": [serialize_lot(lot) for lot in lots]
    }


@app.get("/lots/<lot_id>")
def get_lot(lot_id: str):
    lot = find_lot(bids_table, lot_id)
    return serialize_lot(lot) if lot else None


def serialize_lot(lot):
    return {
        "id": lot.id,
        "name": lot.name,
        "status": lot.status.name,
        "highest_bid_id": lot.highest_bid_id,
        "highest_bid_amount": lot.highest_bid_amount,
        "time_opened": lot.time_opened.isoformat() if lot.time_opened is not None else None,
    }


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
