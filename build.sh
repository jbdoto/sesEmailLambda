#!/bin/bash
TAG=1.0.0
IMAGE_NAME=ses-email-handler
ACCOUNT_URI=483158796244.dkr.ecr.us-east-1.amazonaws.com
REPO_URI=$ACCOUNT_URI/$IMAGE_NAME
IMAGE_URI=$REPO_URI:$TAG

docker build . -t $IMAGE_NAME
docker tag $IMAGE_NAME $IMAGE_URI
aws ecr get-login-password --region us-east-1 --profile=jdoto-ab3 | docker login --username AWS --password-stdin $ACCOUNT_URI
docker push $IMAGE_URI
aws lambda  update-function-code --function-name $IMAGE_NAME --image-uri $IMAGE_URI --publish --profile=jdoto-ab3 --region=us-east-1
