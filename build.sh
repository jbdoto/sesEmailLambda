#!/bin/bash

aws ecr get-login-password --region us-east-1 --profile=jdoto-ab3 | docker login --username AWS --password-stdin 483158796244.dkr.ecr.us-east-1.amazonaws.com
docker build . -t sns-email-handler
docker tag ses-email-handler 483158796244.dkr.ecr.us-east-1.amazonaws.com/ses-email-handler:1.0.0
docker push 483158796244.dkr.ecr.us-east-1.amazonaws.com/ses-email-handler:1.0.0
