import os
import json
import boto3
from fastapi import FastAPI

app = FastAPI()

@app.get('/trigger/{media_id}')
async def trigger_Workflow(media_id: str):
    sfn = boto3.client('stepfunctions', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_ACCESS_SECRET'),region_name=os.environ.get('AWS_REGION'))
    response = sfn.start_execution(
    stateMachineArn='<state_machine_arn>',
        input=json.dumps({"media_id": media_id}),
    )
    return "Success"