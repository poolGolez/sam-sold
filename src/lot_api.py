from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

app = APIGatewayRestResolver()
logger = Logger(service="Lot API")


@app.get("/lots/<lot_id>")
def get_lot(lot_id: str):
    return {
        "lot_id": lot_id,
        "lot": "<TODO>"
    }


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
