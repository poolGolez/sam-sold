import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from dao import find_lot, find_all_lots, find_bids_by_lot

app = APIGatewayHttpResolver()
logger = Logger(service="LotApi")
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


@app.get("/lots/<lot_id>/bids")
def get_bids_by_lot(lot_id: str):
    lot = find_lot(bids_table, lot_id)
    size = int(app.current_event.get_query_string_value("size", "20"))
    start_key = app.current_event.get_query_string_value("next")

    if lot is None:
        return {
            "statusCode": 404,
            "body": f"Lot {lot_id} not found"
        }

    return find_bids_by_lot(bids_table, lot, size=size, start_key=start_key)


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)


def serialize_lot(lot):
    return {
        "id": lot.id,
        "name": lot.name,
        "status": lot.status.name,
        "imageUrl": lot.image_url,
        "highestBidId": lot.highest_bid_id,
        "highestBidAmount": lot.highest_bid_amount,
        "timeOpened": lot.time_opened.isoformat() if lot.time_opened is not None else None,
    }
