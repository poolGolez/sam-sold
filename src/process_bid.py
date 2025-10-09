import json

from aws_xray_sdk.core.lambda_launcher import LambdaContext


def lambda_handler(event: dict, context: LambdaContext):
    for record in event['Records']:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(record)
        body = record['body']
        print(body)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    return { "status": 200 }
