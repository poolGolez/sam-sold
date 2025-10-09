import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import boto3
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

app = APIGatewayRestResolver()
bid_queue_url = os.environ['BID_QUEUE_URL']
sqs = boto3.client('sqs')


@app.post("/bid")
def place_bid():
    body = app.current_event.json_body
    bid = Bid(**{
        **body,
        "time_placed": datetime.now()
    })

    sqs_response = sqs.send_message(
        QueueUrl=bid_queue_url,
        MessageBody=json.dumps(bid.to_json())
    )

    return {
        "message": "Place Bid",
        "body": body,
        "bid": bid.to_json(),
        "queue": bid_queue_url,
        "sqs_response": sqs_response
    }


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)


@dataclass(frozen=True)
class Bid:
    user_id: str
    lot_id: str
    amount: Decimal
    time_placed: datetime
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "timestamp": self.time_placed.isoformat()
        }
