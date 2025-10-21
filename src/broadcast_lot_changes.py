from aws_lambda_powertools import Logger

logger = Logger(service="BroadcastLotChangesService")

@logger.inject_lambda_context
def lambda_handler(event, context):
    for record in event['Records']:
        event_name = record['eventName']
        keys = record['dynamodb']['Keys']
        new_image = record['dynamodb'].get('NewImage', {})
        old_image = record['dynamodb'].get('OldImage', {})

        # print(f"Event: {event_name}")
        # print(f"Keys: {keys}")
        # print(f"Old Image: {old_image}")
        # print(f"New Image: {new_image}")
        logger.info(f"{new_image['PK']['S']} bid increased to {new_image.get('highest_bid_amount', {}).get('N', 0.0)}")

    return {"statusCode": 200}
