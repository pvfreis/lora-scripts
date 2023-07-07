import boto3
from botocore.exceptions import NoCredentialsError

# S3 bucket name and object name
bucket_name = "sai-output1"
object_name = "output_images.zip"

# Email details
SENDER = "Seu Avatar IA <pvfreis@gmail.com>"
RECIPIENT = "renato.tura@eventocircular.com.br"
AWS_REGION = "us-east-2"
SUBJECT = "Seus Avatares estão prontos!"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Clique no link para baixar seus avatares\r\n")

# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
<h1>Clique no link para baixar seus avatares</h1>
<p><a href='{presigned_url}'>Clique aqui</a></p>
</body>
</html>
"""


def create_presigned_url(bucket_name, object_name, expiration=604800):
    """Generate a presigned URL to share an S3 object"""
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        print("No AWS credentials found")
        return None
    return response


def send_email(presigned_url):
    # Update your HTML BODY here with the presigned_url
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Your download link</h1>
    <p><a href='{}'>Download file</a></p>
    </body>
    </html>
    """.format(presigned_url)

    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION)

    try:
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
        )
    except Exception as e:
        print("Error sending email. ", e)
    else:
        print("Email sent! Message Id:", response['MessageId'])


if __name__ == "__main__":
    url = create_presigned_url(bucket_name, object_name)
    if url is not None:
        send_email(url)
