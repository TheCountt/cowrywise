import boto3

elb_client = boto3.client('elbv2')
ec2_client = boto3.client('ec2')

TARGET_GROUP_ARN = TARGET_GROUP_ARN = 'arn:aws:elasticloadbalancing:ap-southeast-2:851725191615:targetgroup/spot-instance-webscrapper-prod/5bb4239ceda003ac'
TARGET_TAG_KEY = "environment"
TARGET_TAG_VALUE = "production"

def lambda_handler(event, context):
    instance_id = event['detail']['instance-id']
    state = event['detail']['state']

    # Check if the instance has any tags
    if not instance_has_tags(instance_id):
        print(f"Instance {instance_id} has no tags. Exiting.")
        return {"statusCode": 200, "body": f"No action for instance {instance_id} without tags"}

    # Register or deregister based on instance state
    if state == 'running':
        register_instance(instance_id)
    elif state == 'terminated':
        deregister_instance(instance_id)
    
    return {"statusCode": 200, "body": f"Action completed for instance {instance_id} with state {state}"}

def instance_has_tags(instance_id):
    """Check if the instance has any tags."""
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    tags = response['Reservations'][0]['Instances'][0].get('Tags', [])
    return bool(tags)

def register_instance(instance_id):
    """Register the instance with the target group."""
    elb_client.register_targets(
        TargetGroupArn=TARGET_GROUP_ARN,
        Targets=[{
            'Id': instance_id, 
            'Port': 3003
        }])
    print(f"Registered instance {instance_id} to target group.")

def deregister_instance(instance_id):
    """Deregister the instance from the target group."""
    elb_client.deregister_targets(
        TargetGroupArn=TARGET_GROUP_ARN,
        Targets=[{
            'Id': instance_id
        }])
    print(f"Deregistered instance {instance_id} from target group.")
 