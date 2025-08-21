import boto3
from utils import get_username, confirm_public_bucket, resource_tagged_by_cli
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
s3_res = boto3.resource('s3')

def handle_s3(action, params):
    username = get_username()

    if action == "create":
        bucket_name = params.get("name")
        if not bucket_name:
            print("ERROR: Provide bucket name via --params name=my-bucket")
            return

        is_public = params.get("public", "false").lower() == "true"
        if is_public and not confirm_public_bucket():
            print("Bucket creation cancelled.")
            return

        s3.create_bucket(Bucket=bucket_name)
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={'TagSet': [{'Key': 'CreatedBy', 'Value': 'platform-cli'},
                                {'Key': 'Owner', 'Value': username}]}
        )

        if is_public:
            s3.put_bucket_acl(Bucket=bucket_name, ACL='public-read')
        print(f"SUCCESS: Bucket {bucket_name} created")

    elif action == "upload":
        bucket = params.get("bucket")
        file_path = params.get("file")
        if not bucket or not file_path:
            print("ERROR: Provide bucket and file path")
            return
        # Only allow upload if CLI created
        tags = s3.get_bucket_tagging(Bucket=bucket)['TagSet']
        if not resource_tagged_by_cli(tags):
            print("ERROR: Bucket not created by CLI")
            return
        key = file_path.split("/")[-1]
        s3.upload_file(file_path, bucket, key)
        print(f"Uploaded {file_path} to {bucket}/{key}")

    elif action == "list":
        buckets = s3.list_buckets()["Buckets"]
        for bucket in buckets:
            try:
                tags = s3.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
                if resource_tagged_by_cli(tags):
                    print(bucket['Name'])
            except:
                continue

    def delete_bucket(params):
    bucket_name = params.get("bucket_name")
    dry_run = str(params.get("dry_run", "false")).lower() == "true"
    force = str(params.get("yes", "false")).lower() == "true"

    if not bucket_name:
        print("Must provide bucket_name for deletion.")
        return

    try:
        if dry_run:
            print(f"[DryRun] Would delete bucket {bucket_name} and all its objects.")
            return

        bucket = s3_res.Bucket(bucket_name)
        objects = list(bucket.objects.all())
        versions = list(bucket.object_versions.all())

        if (objects or versions) and not force:
            print(f" Bucket {bucket_name} is not empty. Use --yes to force delete.")
            return

        # delete objects
        bucket.objects.all().delete()
        bucket.object_versions.all().delete()
        bucket.delete()
        print(f"Bucket {bucket_name} deleted successfully.")
    except ClientError as e:
        print(f"Error deleting bucket: {e}")


