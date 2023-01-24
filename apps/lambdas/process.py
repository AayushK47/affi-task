import json
import urllib3
import boto3

def lambda_handler(message, context):
    http = urllib3.PoolManager()
    base_url = '<base_url>'
    res = http.request("POST", f"{base_url}/process", headers={'Content-Type': 'application/json'}, body=json.dumps(message))
    
    if res.status == 200:
        data = res.data.decode("utf-8")
        print(data)
        if type(data) == dict and data.get('detail') == 'Fail':
            raise Exception('Validation Failed')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('affi_table')
        table_data = table.get_item(Key={'id': message.get('media_id')})
        table_data['Item']['status']['done'].append("process")
        response = table.put_item(Item=table_data['Item'])
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }