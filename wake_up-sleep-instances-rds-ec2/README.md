# Description
Stop/Start EC2 and RDS. Time between RDS startup and EC2 startup can be modified.

#Instruction
The instances must be tagged with the tag: "lambda_sleep_instances" and any value, like "true".

#JSON Policy for the lambda role:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "rds:DescribeDBInstanceAutomatedBackups",
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "ses:SendRawEmail",
                "rds:DescribeDBInstances",
                "rds:StopDBInstance",
                "ec2:StopInstances",
                "rds:StartDBInstance",
                "rds:ListTagsForResource"
            ],
            "Resource": "*"
        }
    ]
}
