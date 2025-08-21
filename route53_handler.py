import boto3
from utils import get_username, resource_tagged_by_cli
from botocore.exceptions import ClientError


client = boto3.client('route53')

r53 = boto3.client("route53")

def handle_route53(action, params):
    try:
        if action == "create":
            domain_name = params.get("domain_name")
            if not domain_name:
                print("❌ Must provide domain_name")
                return
            print(f"Creating hosted zone {domain_name}...")
            r53.create_hosted_zone(
                Name=domain_name,
                CallerReference=domain_name
            )

        elif action == "delete":
            hosted_zone_id = params.get("hosted_zone_id")
            dry_run = str(params.get("dry_run", "false")).lower() == "true"
            force = str(params.get("yes", "false")).lower() == "true"

            if not hosted_zone_id:
                print("❌ Must provide hosted_zone_id")
                return

            rrsets = r53.list_resource_record_sets(HostedZoneId=hosted_zone_id)["ResourceRecordSets"]
            changes = []
            for rr in rrsets:
                if rr["Type"] in ("NS", "SOA"):
                    continue
                changes.append({"Action": "DELETE", "ResourceRecordSet": rr})

            if dry_run:
                print(f"[DryRun] Would delete hosted zone {hosted_zone_id} with {len(changes)} records.")
                return

            if changes and not force:
                print(f"❌ Hosted zone not empty. Use --yes to confirm deletion.")
                return

            if changes:
                r53.change_resource_record_sets(
                    HostedZoneId=hosted_zone_id,
                    ChangeBatch={"Changes": changes}
                )

            r53.delete_hosted_zone(Id=hosted_zone_id)
            print(f"Hosted zone {hosted_zone_id} deleted successfully.")

        elif action == "list":
            zones = r53.list_hosted_zones()
            for z in zones.get("HostedZones", []):
                print(z["Id"], z["Name"])

        else:
            print(f"Unknown Route53 action: {action}")

    except ClientError as e:
        print(f"Error handling Route53: {e}")

