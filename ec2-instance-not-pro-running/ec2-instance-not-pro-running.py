import boto3
import json
 
ec2 = boto3.client('ec2')
ids = []
 
def lambda_handler(event, context):
    list_instances()
    print(len(ids))
    if len(ids) > 0:
        raise NameError('Instancias que no son de pro activadas!')
    return True

def list_instances():
    reservations = ec2.describe_instances(
        Filters = [
                {'Name': 'tag-key', 'Values': ['not-pro']}
            ]
        ).get('Reservations', [])
    instances = sum(
            [
                [i for i in r['Instances']]
                for r in reservations
            ], []
        )
    
    for instance in instances:
        if instance['State']['Name'] != 'stopped':
            ids.append(instance['InstanceId'])
