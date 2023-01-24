import boto3
import json
import urllib3

def lambda_handler(message, context):
    http = urllib3.PoolManager()
    base_url = 'https://cd76-223-190-95-180.in.ngrok.io'
    res = http.request('GET', f'{base_url}/is_valid_media_id/{message.get("media_id")}')
    data = res.data.decode("utf-8")
    
    
    if type(data) == dict and data['detail'] == 'Fail':
        return {
            'statusCode': 400,
            'body': "Invalid id"
        }
    else:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('affi_table')
        data = {"id": message.get('media_id'), "status": {"done": ["is_valid_media_id"] }}
        table.put_item(Item=data)
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
        
    # TODO implement
