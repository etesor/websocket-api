import logging
import os
import boto3
import json


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    route_key = event.get('requestContext', {}).get('routeKey')
    connection_id = event.get('requestContext', {}).get('connectionId')

    logger.info("PutWords started. route_key: %s, connection_id: %s", route_key, connection_id)

    if table_name is None or route_key is None or connection_id is None:
        return {'statusCode': 400}

    table = boto3.resource('dynamodb').Table(table_name)
    logger.info("Request: %s, use table %s.", route_key, table.name)

    if route_key == 'putwords':
        domain = event.get('requestContext', {}).get('domainName')
        stage = event.get('requestContext', {}).get('stage')

        apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')

        body = event.get('body')
        body = json.loads(body)

        # Upload to DynamoDB
        with table.batch_writer() as batch:
            # Loop through the JSON objects
            for word in body['data']:
                batch.put_item(Item={'word': word})

        apig_management_client.post_to_connection(
            Data='Upload finished?', ConnectionId=connection_id
        )

    return {"statusCode": 200}
