import boto3
from utils import get_username, resource_tagged_by_cli, get_latest_ami
from config import ALLOWED_INSTANCE_TYPES
from botocore.exceptions import ClientError


ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def handle_ec2(action, params):
    username = get_username()

    if action == "create":
        instance_type = params.get("type", "t3.micro")
        if instance_type not in ALLOWED_INSTANCE_TYPES:
            print(f"ERROR: Instance type '{instance_type}' not allowed.")
            return

        running_instances = list(ec2.instances.filter(
            Filters=[{'Name': 'tag:CreatedBy', 'Values': ['platform-cli']},
                     {'Name': 'instance-state-name', 'Values': ['running']}]))
        if len(running_instances) >= 2:
            print("ERROR: Max 2 running instances allowed.")
            return

        ami = get_latest_ami(params.get("os", "ubuntu"))
        instance = ec2.create_instances(
            ImageId=ami,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'CreatedBy', 'Value': 'platform-cli'},
                         {'Key': 'Owner', 'Value': username}]
            }]
        )[0]
        print(f"SUCCESS: Created instance {instance.id}")

    elif action in ["start", "stop"]:
        for instance in ec2.instances.all():
            if resource_tagged_by_cli(instance.tags):
                if action == "start":
                    instance.start()
                    print(f"Started: {instance.id}")
                elif action == "stop":
                    instance.stop()
                    print(f"Stopped: {instance.id}")

    elif action == "list":
        for instance in ec2.instances.all():
            if resource_tagged_by_cli(instance.tags):
                print(f"{instance.id} | {instance.state['Name']} | {instance.instance_type}")

    elif action == "delete":
        # Get all instances
        instances = ec2.instances.all()

        # Filter instances that are stopped
        deletable_instances = [i for i in instances if i.state['Name'] == 'stopped']

        if not deletable_instances:
            print("No stopped instances found to delete.")
            return

        for instance in deletable_instances:
            try:
                print(f"Terminating instance {instance.id} (state: {instance.state['Name']})")
                instance.terminate()
            except ClientError as e:
                print(f"Error terminating instance {instance.id}: {e}")

        return
