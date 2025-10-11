import json
import os
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from domain import Bid

app = APIGatewayRestResolver()
bid_queue_url = os.environ['BID_QUEUE_URL']
sqs = boto3.client('sqs')
logger = Logger(service="BidService")


@app.post("/bid")
def place_bid():
    body = app.current_event.json_body
    bid = Bid(**{
        **body,
        "time_placed": datetime.now(),
        "time_processed": None
    })

    sqs_response = sqs.send_message(
        QueueUrl=bid_queue_url,
        MessageBody=json.dumps(bid.to_json())
    )
    logger.info("Successfully placed bid", extra={"bid_id": bid.id})

    return {
        "message": "Place Bid",
        "body": body,
        "bid": bid.to_json(),
        "queue": bid_queue_url,
        "sqs_response": sqs_response
    }


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
