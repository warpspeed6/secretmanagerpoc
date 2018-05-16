#!/usr/bin/python

'''
Connects to RDS DB using credential stored in Secret Manager and prints the result
of the query
'''


import boto3
import json
from botocore.exceptions import ClientError
import pymysql


def run_query():
    secret_name = "/poc/MySQL/secretmanager"
    endpoint_url = "https://secretsmanager.ap-southeast-2.amazonaws.com"
    region_name = "ap-southeast-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
    else:
        # Decrypted secret using the associated KMS CMK
        # Depending on whether the secret was a string or binary, one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']

        secret = json.loads(secret)

        username = secret['username']
        engine = secret['engine']
        host = secret['host']
        password = secret['password']
        dbname = secret['dbname']
        dbInstanceIdentifier = secret['dbInstanceIdentifier']

    conn = pymysql.connect(host=host, port=3306, user=username, passwd=password, db=dbname)

    cur = conn.cursor()

    cur.execute("SELECT * FROM anshu")

    for row in cur:
        print row

    cur.close()
    conn.close()

run_query()
