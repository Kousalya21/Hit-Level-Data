aws s3api put-object \
    --bucket hitleveldata-revenue-s3 \
    --key kousalya/scriptLambda.zip \
    --body scriptLambda.zip

aws lambda update-function-code \
    --function-name keywordrevenuefinder \
    --s3-bucket hitleveldata-revenue-s3 \
    --s3-key kousalya/scriptLambda.zip \
    --publish \
    --region us-east-1


