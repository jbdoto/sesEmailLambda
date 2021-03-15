import json
import os
from json2html import *
import boto3
from botocore.exceptions import ClientError
import time
from datetime import timedelta

def send_email(event):
    job_status = event['detail']['status']
    job_name = event['detail']['jobName']
    job_id = event['detail']['jobId']
    job_create_time = event['detail']['createdAt']
    job_start_time = event['detail']['startedAt']
    job_end_time = event['detail']['stoppedAt']
    job_elapsed_time = job_end_time - job_start_time

    print("Got values: %s, %s, %s, %s", job_create_time, job_start_time, job_end_time, job_elapsed_time)

    job_create_time_hr = time.strftime("%Y-%m-%d %I:%M:%S", time.localtime(job_create_time / 1000))
    job_start_time_hr = time.strftime("%Y-%m-%d %I:%M:%S", time.localtime(job_start_time / 1000))
    job_end_time_hr = time.strftime("%Y-%m-%d %I:%M:%S", time.localtime(job_end_time / 1000))
    job_elapsed_time_hr = str(timedelta(seconds=(job_elapsed_time / 1000)))

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

    table = json2html.convert(json=event)

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Bushman Lab IntSiteCaller Batch Job Report</h1>
      <br/>
      <p> Job Took: %s </p>
      <p> Job Create Time: %s </p>
      <p> Job Start Time: %s </p>
      <p> Job End Time: %s </p>
      <a href='https://console.aws.amazon.com/batch/v2/home?region=us-east-1#jobs/detail/%s'>View job details in console.</a>
      <br/>
      <br/>
      <div>%s</div>
    </body>
    </html>
                """ % (job_elapsed_time_hr, job_create_time_hr, job_start_time_hr, job_end_time_hr, job_id, table)

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
