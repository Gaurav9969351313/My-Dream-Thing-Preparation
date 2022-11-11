import boto3
region = 'ap-south-1'
instances = ['i-0c80446a80774bd58']
def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))
