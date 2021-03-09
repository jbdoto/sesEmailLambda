import json
import os

import boto3
from botocore.exceptions import ClientError


def send_email(event):
    job_status = event['detail']['status']
    job_name = event['detail']['jobName']
    job_id = event['detail']['jobId']

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = os.environ['FROM_ADDRESS']

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = os.environ['TO_ADDRESS']

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "intSiteCaller Job %s has %s" % (job_name, job_status)

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Bushman Lab IntSiteCaller Batch Job Report\r\n")

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Bushman Lab IntSiteCaller Batch Job Report</h1>
      <p>intSiteCaller Job %s has %s
        <a href='https://console.aws.amazon.com/batch/v2/home?region=us-east-1#jobs/detail/%s'>Check job</a>
      </p>
    </body>
    </html>
                """ % (job_name, job_status, job_id)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    send_email(event)
