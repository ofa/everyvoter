"""Functionality that sends composed emails"""
from django.conf import settings
import boto3


# pylint: disable=invalid-name
client = boto3.client(
    'ses',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_DEFAULT_REGION)


def deliver(to_address, from_address, subject, html, tags=None):
    """Deliver an email through a mailserver

    Sends an email through SES (or perhaps down the line sendgrid) and returns
    the ID of the mesage.

    Args:
        to_address: email address to send to
        from_address: from address
        subject: subject line
        html: [description]
        tags: key/value tags to be sent with the message (optional)

    Returns:
        message id
        string
    """

    if not tags:
        tags = {}
    else:
        # Tags could be any format that can be turned into a dictionary
        tags = dict(tags)

    tags['app'] = settings.APP_NAME


    # Boto expects tags in the format [{'Name': 'name', 'Value': 'value'}]
    final_tags = [{
        'Name': unicode(k).encode("utf-8"),
        'Value': unicode(v).encode("utf-8")
        } for k, v in tags.iteritems()]

    response = client.send_email(
        Source=from_address,
        Destination={
            'ToAddresses': [
                unicode(to_address).encode("utf-8"),
            ],
        },
        Message={
            'Subject': {
                'Data': unicode(subject).encode("utf-8"),
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Data': unicode(html).encode("utf-8"),
                    'Charset': 'UTF-8'
                }
            }
        },
        Tags=final_tags,
        ConfigurationSetName=settings.SES_CONFIGURATIONSET_NAME
    )
    return response['MessageId']
