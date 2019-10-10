This script detects instances with a label "not-pro" and if there are running raises one exception that can be readed by AWS Cloudwatch and make other automatized action.
The role for the lambda have the AWS Policy for Basic Execution and a custom policy that is in policy.json file.
