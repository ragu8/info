import os
import json
import boto3
import urllib.parse
from ExtractText.Models import DocumentStatus
from ExtractText.Services import DBServices, AWSTextractService, S3Services, EmailNotificationService

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        snsarn = os.environ.get('aws_sns_arn')
        MyConString = "server=sims.cluster-c9ymh2kvopt7.us-east-1.rds.amazonaws.com;database=SIMS;uid=sims_admin;pwd=ljrFDGLMLZGoXtcGticz"
        archiveFolder = os.environ.get('archive')
        awsAccessKey = os.environ.get('aws_access_key')
        awsSecratKey = os.environ.get('aws_secrat_key')
        destinationBucket = os.environ.get('destination_bucket_name')
        sourceBucket = event['Records'][0]['s3']['bucket']['name']
        fileName = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
        context.logger.log("Step 1: Get file byte data started")
        fileData = await GetObjectAsync(context, event)
        context.logger.log("Step 1: Get file byte data done")
        file = os.path.basename(fileName)
        pdfFileName = os.path.splitext(file)[0]
        context.logger.log("Step 5: Get process file status form db started")
        context.logger.log(f"FileName for db search:{fileName.replace('+', ' ').replace('%2C+', ',')}")
        doc = DBServices.GetDocumentStatus(fileName.replace('+', ' ').replace('%2C+', ', '), MyConString)
        context.logger.log(f"Step 5: Get process file status form db done, pagenumber {json.dumps(doc)}")
        FilePath = f"https://sims-input.s3.amazonaws.com/{archiveFolder}/{doc.DocumentName}"
        ImageFilePath = f"https://{destinationBucket}.s3.amazonaws.com/{fileName}"
        if fileData and doc:
            context.logger.log("Step 2: Calling textract aws api started")
            jobj = await AWSTextractService.GetAWSTextractData(fileData)
            context.logger.log(f"Step 2: Calling textract aws api done {json.dumps(jobj)}")
            if jobj:
                context.logger.log("Step 3: Calling Db services to insert aws api response stared")
                result = DBServices.InsertDocumentData(doc.CreatedBy, fileName, json.dumps(jobj), MyConString, doc.PageNumber, FilePath, ImageFilePath, doc.DocumentName)
                context.logger.log("Step 3: Calling Db services to insert aws api response done")
                context.logger.log(f"Step 4: Copy process file form from {sourceBucket} stared")
                await S3Services.CopyS3BucketFiles(fileName, sourceBucket, destinationBucket, awsAccessKey, awsSecratKey, context)
                context.logger.log(f"Step 4: Copy process file form from {sourceBucket} stared")
                if doc.IsLastPage:
                    context.logger.log(f"Step 7:Email Notification stared with {doc.DocumentName}")
                    client = boto3.client('sns', region_name='us-east-1')
                    EmailNotificationService.SendMessage(client, doc.DocumentName, snsarn).wait()
                    context.logger.log(f"Step 7:Email Notification done")
                    context.logger.log(f"Step 8:DB Status update started")
                    DBServices.UpdateDocumentStatus(doc.DocumentName, MyConString)
                    context.logger.log(f"Step 8:DB Status update done")
                context.logger.log(f"Step 6: File deletion form bucket {sourceBucket} started")
            await S3Services.DeleteS3BucketFiles(fileName, sourceBucket, destinationBucket, awsAccessKey, awsSecratKey, context)
            context.logger.log(f"Step 6: File deletion form bucket {sourceBucket} done")
        return ""
    except Exception as e:
        context.logger.log(f"Error processing request - {e}")
        return ""

async def GetObjectAsync(context, event):
    context.logger.log("Lambda exectecution started - Extract API")
    context.logger.log(f"S3 recvied object : {json.dumps(event)}")
    data = None
    if len(event['Records']) <= 0:
        context.logger.log("Empty S3 Event received")
        return None
    context.logger.log("Lambda exectecution started")
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
    context.logger.log(f"Request process for buket \n: {bucket} and and file name \n:{key}")
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read()
    except ClientError as e:
        context.logger.log(f"Error getting object {key} from bucket {bucket}: {e}")
    return data

