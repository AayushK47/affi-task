import os
import json
import boto3
import requests
from .schemas import IsValidMediaIdRequest, ProcessRequest
from fastapi import FastAPI

app = FastAPI()

@app.post('/process')
async def process(body: ProcessRequest):
    media_id = body.media_id
    access_token = os.environ['ACCESS_TOKEN']
    s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_ACCESS_SECRET'),region_name=os.environ.get('AWS_REGION'))

    url = f"https://graph.instagram.com/v15.0/{body.media_id}?fields=id,caption,media_url,media_type,permalink,thumbnail_url,timestamp,username,like_count,comment_count&access_token={access_token}"
    response = requests.get(url)
    # Benefit here would be that rate limiting from insta api will not be an issue
    # Also we would not have to require the instagram access token every time we fetch the data
    data = response.json()
    media = response.json().get('media_url')
    r = requests.get(media, stream=True)
    bucket = s3.Bucket('affi-task-s3-bucket')
    bucket.upload_fileobj(r.raw, f'{media_id}/{media_id}_media')
    file_size = len(r.content) * 0.000001
    data['size'] = file_size + data['like_count'] + data['comment_count']
    data['Score'] = file_size

    bucket.put_object(Body=json.dumps(data), Key=f'{media_id}/metadata')
    return "Success"
    
@app.get('/is_valid_media_id/{id}')
async def is_valid_media_id(id: str):
    id = IsValidMediaIdRequest.parse_obj({ "id": id })
        
    return "Success"