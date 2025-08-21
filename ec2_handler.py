import boto3
from utils import get_username, resource_tagged_by_cli, get_latest_ami
from config import ALLOWED_INSTANCE_TYPES
from botocore.exceptions import ClientError

ec2 = boto3.resource("ec2")


def handle_ec2(action, params):
    try:
        if action == "create":
            instance_type = params.get("instance_type", "t3.micro")
            print(f"Creating EC2 instance of type {instance_type}...")
            ec2.create_instances(
                ImageId="ami-1234567890abcdef0",  # עדכן ל-AMI אמיתי
                MinCount=1,
                MaxCount=1,
                InstanceType=instance_type,
                TagSpecifications=[{
                    "ResourceType": "instance",
                    "Tags": [{"Key": "CreatedBy", "Value": "platform-cli"}]
                }]
            )

        elif action == "delete":
            instance_id = params.get("instance_id")
            all_tagged = str(params.get("all_tagged", "false")).lower() == "true"
            dry_run = str(params.get("dry_run", "false")).lower() == "true"
            force = str(params.get("yes", "false")).lower() == "true"

            if instance_id:
                if dry_run:
                    print(f"[DryRun] Would terminate instance {instance_id}")
                    return
                ec2.Instance(instance_id).terminate()
                print(f"Instance {instance_id} terminated.")
            elif all_tagged:
                instances = ec2.instances.filter(Filters=[
                    {"Name": "tag:CreatedBy", "Values": ["platform-cli"]}
                ])
                ids = [i.id for i in instances]
                if not ids:
                    print("No instances found to delete.")
                    return
                if not force:
                    print("❌ Refusing to delete multiple instances without --yes")
                    return
                if dry_run:
                    print(f"[DryRun] Would terminate instances: {ids}")
                    return
                for iid in ids:
                    ec2.Instance(iid).terminate()
                    print(f"Instance {iid} terminated.")
            else:
                print("❌ Must specify either instance_id or all_tagged=true")

        elif action == "list":
            for i in ec2.instances.all():
                print(i.id, i.state)

        else:
            print(f"Unknown EC2 action: {action}")

    except ClientError as e:
        print(f"Error handling EC2: {e}")



