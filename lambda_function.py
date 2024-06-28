import boto3
import uuid

dynamodb = boto3.resource('dynamodb',
        aws_access_key_id='AKIA56SSZ7JKEMJJGNEJ',
        aws_secret_access_key='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',
        region_name='us-east-1')

table = dynamodb.Table('sandy')
ses = boto3.client('ses',
         aws_access_key_id='AKIA56SSZ7JKEMJJGNEJ',
        aws_secret_access_key='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',
        region_name='us-east-1')

def lambda_handler(event, context):
    emails = event['emails']
    filename = event['filename']
    sender_email = "sandeepsunny061@gmail.com"  
    subject = "File Sharing Notification"
    body = f"Hello user,\n\nA file '{filename}' is sent to you.\n\n please access using the link: https://sandeep46.s3.us-east-1.amazonaws.com/{filename}\n\n Regards,\nSandeep Vanaparthi"


    response = ses.send_email(
        Source=sender_email,
        Destination={'ToAddresses': emails},
        Message={
            'Subject': {'Data':subject},
            'Body': {'Text': {'Data': body}},
        }
    )
        
    ID = str(uuid.uuid4())
        
    file_info = {
    'fileid': ID,  
    'FileName': filename
    }
    table.put_item(Item=file_info)
        