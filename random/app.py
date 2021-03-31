import logging
import os
import boto3
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_random(table):
    response = table.scan()
    logger.info("DB scan result: %s", response)
    response = response['Items']
    # logger.info(response)

    randitem = random.choice(response)['word']
    logger.info("Random word is: %s", randitem)
    return randitem


def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    route_key = event.get('requestContext', {}).get('routeKey')
    connection_id = event.get('requestContext', {}).get('connectionId')

    logger.info("Invocation started. route_key: %s, connection_id: %s", route_key, connection_id)

    if table_name is None or route_key is None or connection_id is None:
        return {'statusCode': 400}

    table = boto3.resource('dynamodb').Table(table_name)
    # logger.info("Request: %s, use table %s.", route_key, table.name)

    if route_key == 'getrandom':
        domain = event.get('requestContext', {}).get('domainName')
        stage = event.get('requestContext', {}).get('stage')

        apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
        randomized = get_random(table)
        message = f"word: {randomized}"
        apig_management_client.post_to_connection(
            Data=message, ConnectionId=connection_id
        )

    return {"statusCode": 200}
