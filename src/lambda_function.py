import json
import datetime
import boto3
import ssl
import socket
import os


from typing import List, Dict

def lambda_handler(event, context):
    # Initialize an SNS client
    sns = boto3.client('sns')

    # prd has different hostname syntax than others
    if os.environ["environment"] == 'prd':
      hostname = 'api.move.mil'
    else:
      hostname = f'api.{os.environ["environment"]}.{os.environ["zone"]}'

    # Need 90 day notice for ATO environments, can get away with 30 for non-ATO
    days_to_notify = 90
    if os.environ["zone"] == 'dp3.us':
        days_to_notify = 30

    # List of hostnames, port numbers, and number of days to notify before expiration
    hosts = [
        {'hostname': hostname, 'port': 443, 'days_to_notify': days_to_notify}
    ]

    for host in hosts:
        try:
            hostname = host['hostname']
            port = host['port']
            days_to_notify = host['days_to_notify']
            ssl_context = ssl.create_default_context()
            if os.environ["zone"] == 'move.mil':
                ssl_context.load_verify_locations('DoD_CAs.pem')

            conn = ssl_context.wrap_socket(
                socket.create_connection((hostname, port)),
                server_hostname=hostname,
            )
            cert = conn.getpeercert()
            exp = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            exp_time = (exp - datetime.datetime.utcnow()).total_seconds()

            print(f'Lambda - CheckSSL - INFO - {hostname} SSL certificate will expire on {exp}')

            if exp_time <= days_to_notify * 24 * 60 * 60:
                sns.publish(
                    TopicArn=f'arn:aws-us-gov:sns:us-gov-west-1:{os.environ["account_id"]}:infra-gov-alert',
                    Message=f'Lambda - CheckSSL - WARN - {hostname} SSL certificate will expire in less than {days_to_notify} days.'
                )
                print(f'Lambda - CheckSSL - WARN - {hostname} SSL certificate will expire in less than {days_to_notify} days')
        except Exception as e:
            print(f'Lambda - CheckSSL - ERROR - Error checking {hostname} SSL certificate expiration: {e}')