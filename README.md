# sesEmailLambda


https://docs.aws.amazon.com/lambda/latest/dg/images-create.html

https://docs.aws.amazon.com/lambda/latest/dg/images-test.html

https://docs.aws.amazon.com/lambda/latest/dg/python-image.html


Note: for the purposes of demonstration, I manually created an SES address valid only for my personal email.

https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-getting-started.html


A full setup would require some additional time, though this might make it easier:

https://binx.io/blog/2019/11/14/how-to-deploy-aws-ses-domain-identities-dkim-records-using-cloudformation/


### Testing

    docker build . -t ses-email-handler:latest

    # default region is used by boto to configure step client
    docker run -e AWS_DEFAULT_REGION=us-east-1 -e AWS_REGION=us-east-1 -e AWS_ACCESS_KEY_ID=<key_id> \
        -e AWS_SECRET_ACCESS_KEY=<key> -p 9000:8080  ses-email-handler:latest

    # test with empty post body:
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

    # or post with data from json file:
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '@sns_event_message.json'

### Pushing to ECR

    aws ecr get-login-password --region us-east-1 --profile=jdoto-ab3 \
    | docker login --username AWS --password-stdin 483158796244.dkr.ecr.us-east-1.amazonaws.com

    docker tag ses-email-handler 483158796244.dkr.ecr.us-east-1.amazonaws.com/ses-email-handler:1.0.0

    docker push 483158796244.dkr.ecr.us-east-1.amazonaws.com/ses-email-handler:1.0.0


