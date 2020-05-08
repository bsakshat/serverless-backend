import json
import boto3
import uuid
import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Survey')

def lambda_handler(event, context):
    # TODO implement
    if event["httpMethod"] == "GET":
        if (event["pathParameters"]):
            data = get(event)
        else:
            data = getAll(event)
    elif event["httpMethod"] == "POST":
        data = add(event)
    else:
        response = {
        "statusCode": 500,
        "body": json.dumps('Method Not Supported')
        }
        return response
    
    response = {
        "statusCode": 200,
        "body": data,
        "headers": {
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Content-Type': 'application/json'
        }
    }
    return response

def get(event):
    id = event["pathParameters"]
    result = table.get_item(
        Key={
            "StudentId": id
        }
    )
        
    del result["Item"]["StudentId"]
    
    response = result["Item"]
    
    return response
    
    
def add(event):
    data = event['body']
    
    data['StudentId'] = int(uuid.uuid4()) % 100
    
    table.put_item(Item=data)
    
    response = {
        "statusCode": 200,
        "body": json.dumps('Survey Added')
    }
    
    return response
    
    
def getAll(event):
    result = table.scan()
    
    ids = list(map(lambda datum: str(datum['StudentId']), result['Items']))
    
    #response = json.dumps(ids, cls=decimalencoder.DecimalEncoder)
    
    return ids