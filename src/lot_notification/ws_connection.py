def lambda_handler(event, context):
    print("Connect event:", event)
    connection_id = event['requestContext']['connectionId']
    return {
        "statusCode": 200,
        "body": f"Connected: {connection_id}"
    }
