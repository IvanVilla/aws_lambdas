#!/bin/python

import boto3

type_finder=["t2","m4","r4"]

for instance_type in type_finder:
    print("========== Tipo buscado: " + instance_type + " ==========")
    print("Buscando EC2...")
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if (instance_type in instance.instance_type):
            print(
                    "Id: {}, Type: {}"
                    .format(
                        instance.id,
                        instance.instance_type
                        )
                    )
    print("Buscando Reservas EC2...") 
    reserved_ec2 = boto3.client('ec2')
    response = reserved_ec2.describe_reserved_instances()['ReservedInstances']
    for reserve in response:
        if (instance_type in reserve['InstanceType'] and reserve['State'] != 'retired'):
            print(
                    "Id: {}, Type: {}, Count: {}"
                    .format(
                        reserve['ReservedInstancesId'],
                        reserve['InstanceType'],
                        reserve['InstanceCount']
                        )
                    )
    print("Buscando RDS...")
    rds = boto3.client('rds')
    response = rds.describe_db_instances()['DBInstances']
    for instance in response:
        if (instance_type in instance['DBInstanceClass']):
            print(
                    "Id: {}, Type: {}"
                    .format(
                            instance['DBInstanceIdentifier'],
                            instance['DBInstanceClass']
                            )
                    )
    print("Buscando Reservas RDS...")
    response = rds.describe_reserved_db_instances()
    for reserve in response['ReservedDBInstances']:
        if (instance_type in reserve['DBInstanceClass'] and reserve['State'] != 'retired'):
            print(
                    "Id: {}, Type: {}, Count: {}"
                    .format(
                        reserve['ReservedDBInstanceId'],
                        reserve['DBInstanceClass'],
                        reserve['DBInstanceCount']
                        )
                    )
            
