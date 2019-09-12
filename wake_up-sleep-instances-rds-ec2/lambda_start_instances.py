import boto3
import json
import time
 
ec2 = boto3.client('ec2')
rds = boto3.client('rds')
ids_ec2 = []
ids_rds = []

# Time wait between RDS start and EC2 start
waiting_time = 600
 
def lambda_handler(event, context):
    list_instances_rds()
    try:
        start_instances_rds()
        time.sleep(waiting_time)
    except:
        pass
    list_instances_ec2()
    try:
        start_instances_ec2()
    except:
        pass
    return True

def list_instances_rds():
    dbs = []
    reservations = rds.describe_db_instances()
    for reservation in reservations['DBInstances']:
        dbs.append(reservation['DBInstanceArn'])
    for db_name in dbs:
        response = rds.list_tags_for_resource(ResourceName=db_name)
        for tag in response['TagList']:
            if tag['Key'] == 'lambda_sleep_instances':
                ids_rds.append(db_name.split("db:")[1])

def start_instances_rds():
    for db in ids_rds:
        rds.start_db_instance(DBInstanceIdentifier=db)

     
def list_instances_ec2():
    reservations = ec2.describe_instances(
        Filters = [
                {'Name': 'tag-key', 'Values': ['lambda_sleep_instances']}
            ]
        ).get('Reservations', [])
    instances = sum(
            [
                [i for i in r['Instances']]
                for r in reservations
            ], []
        )
    for instance in instances:
        ids_ec2.append(instance['InstanceId'])
 
def start_instances_ec2():
    ec2.start_instances(InstanceIds=ids_ec2)
