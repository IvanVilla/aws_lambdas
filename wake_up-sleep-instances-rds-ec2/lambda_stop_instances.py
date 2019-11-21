import boto3
import json
import time

ec2 = boto3.client('ec2')
rds = boto3.client('rds')
ids_ec2 = []
ids_rds = []
# Time wait between EC2 stop and RDS start
waiting_time = 600
 
def lambda_handler(event, context):
    list_instances_ec2()
    try:
        stop_instances_ec2()
    except:
        pass
    time.sleep(waiting_time)
    list_instances_rds()
    try:
        stop_instances_rds()
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
    
def stop_instances_rds():
    for db in ids_rds:
        rds.stop_db_instance(DBInstanceIdentifier=db)

     
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
 
def stop_instances_ec2():
    ec2.stop_instances(InstanceIds=ids_ec2)
