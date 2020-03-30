from flask import current_app, render_template
import boto3
from botocore.exceptions import ClientError


def send_email(to, subject, template, **kwargs):
    """Function to send email for user confirmations/updates, uses
    a threading model to not offload the processing from the main
    thread"""

    client = boto3.client('ses', region_name=current_app.config['AWS_REGION_NAME'],
                          aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    to,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': render_template(template + '.html', **kwargs),
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': render_template(template + '.txt', **kwargs),
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source='spencer.porter@offbrand.co',
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])
    return True