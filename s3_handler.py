import boto3
from utils import get_username, confirm_public_bucket, resource_tagged_by_cli
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")
s3_res = boto3.resource("s3")

def handle_s3(action, params):
    try:
        if action == "create":
            bucket_name = params.get("bucket_name")
            if not bucket_name:
                print("❌ Must provide bucket_name")
                return
            print(f"Creating bucket {bucket_name}...")
            s3_client.create_bucket(Bucket=bucket_name)

        elif action == "delete":
            bucket_name = params.get("bucket_name")
            dry_run = str(params.get("dry_run", "false")).lower() == "true"
            force = str(params.get("yes", "false")).lower() == "true"

            if not bucket_name:
                print("❌ Must provide bucket_name for deletion.")
                return

            bucket = s3_res.Bucket(bucket_name)
            objects = list(bucket.objects.all())
            versions = list(bucket.object_versions.all())

            if dry_run:
                print(f"[DryRun] Would delete bucket {bucket_name} with {len(objects)} objects and {len(versions)} versions.")
                return

            if (objects or versions) and not force:
                print(f"❌ Bucket {bucket_name} not empty. Use --yes to force delete.")
                return

            bucket.objects.all().delete()
            bucket.object_versions.all().delete()
            bucket.delete()
            print(f"Bucket {bucket_name} deleted successfully.")

        elif action == "list":
            buckets = s3_client.list_buckets()
            for b in buckets.get("Buckets", []):
                print(b["Name"])

        else:
            print(f"Unknown S3 action: {action}")

    except ClientError as e:
        print(f"Error handling S3: {e}")

