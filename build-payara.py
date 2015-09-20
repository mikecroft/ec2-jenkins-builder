#!/usr/bin/python3

import boto3.ec2
import configparser

secrets = configparser.ConfigParser()
secrets.read('.secrets.ini')

print(secrets['AWS_SECRET_ACCESS_KEY'])

conn = boto3.ec2.connect_to_region("eu-west-1", aws_access_key_id=secrets['AWS_ACCESS_KEY_ID'], aws_secret_access_key=secrets['AWS_SECRET_ACCESS_KEY'])

jenkins = conn.get_all_instances(instance_ids=['i-f5095b58'])
print(jenkins.start())
