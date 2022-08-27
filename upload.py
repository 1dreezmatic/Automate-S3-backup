import boto3
from botocore.exceptions import ClientError
from datetime import date

def upload_file_to_s3(file_name, bucket, object_name=None, folder_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name.split('/')[-1]
        # If folder_name was specified, upload in the folder
        if folder_name is not None:
            today = date.today().strftime('%Y/%m/%d')
            object_name = f'{folder_name}/{object_name}/{today}.gz'

    # Upload the file
    try:
        # It would be "s3_client = boto3.client('s3')" if you have AWS CLI configured on the server already
        s3_client = boto3.client(
            service_name='s3',
            aws_access_key_id=YOUR_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=YOUR_AWS_SECRET_ACCESS_KEY
        )
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        print(e)

def backup_logs_to_s3():
	# specify file to look for
    log_files = [
        '/var/log/Nginx/Error.log.1.gz'
    ]

    print('Uploading logs to S3...')
    # use date to group files by year, month and day
    Today = date.today().strftime('%Y/%m/%d')
    # loop used in case of multiple files
    for log_file in log_files:
        upload_file_to_s3(
            file_name=log_file,
            bucket= BUCKET_NAME,
            object_name = f'{ServerName}/{Today}.gz'
        )
    print('Uploaded logs to S3...')
# ensure it's not executed directly when imported
if _name_ == "_main_":
    backup_logs_to_s3()
