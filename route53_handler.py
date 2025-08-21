import boto3
from utils import get_username, resource_tagged_by_cli

client = boto3.client('route53')

def handle_route53(action, params):
    username = get_username()

    if action == "create":
        domain_name = params.get("name")
        if not domain_name:
            print("ERROR: Provide domain via --params name=example.com")
            return

        response = client.create_hosted_zone(
            Name=domain_name,
            CallerReference=str(hash(domain_name)),
            HostedZoneConfig={
                'Comment': 'Created by platform-cli',
                'PrivateZone': False
            },
            Tags=[{'Key': 'CreatedBy', 'Value': 'platform-cli'},
                  {'Key': 'Owner', 'Value': username}]
        )
        print(f"Created zone: {response['HostedZone']['Id']}")

    elif action == "list":
        zones = client.list_hosted_zones()["HostedZones"]
        for zone in zones:
            zone_id = zone['Id']
            tags = client.list_tags_for_resource(ResourceType='hostedzone', ResourceId=zone_id.split("/")[-1])['ResourceTagSet']['Tags']
            if resource_tagged_by_cli(tags):
                print(zone['Name'])

    elif action == "delete":
        hosted_zone_id = params.get("hosted_zone_id")
        if not hosted_zone_id:
            print("Error: 'hosted_zone_id' parameter is required for delete action.")
            return

        try:
            # List all record sets except NS and SOA (required for hosted zone)
            paginator = client.get_paginator('list_resource_record_sets')
            records_to_delete = []

            for page in paginator.paginate(HostedZoneId=hosted_zone_id):
                for record in page['ResourceRecordSets']:
                    # Skip default NS and SOA records
                    if record['Type'] in ['NS', 'SOA']:
                        continue
                    records_to_delete.append({
                        'Action': 'DELETE',
                        'ResourceRecordSet': record
                    })

            # If there are records to delete, submit a change batch
            if records_to_delete:
                print(f"Deleting {len(records_to_delete)} DNS records from hosted zone {hosted_zone_id}...")
                response = client.change_resource_record_sets(
                    HostedZoneId=hosted_zone_id,
                    ChangeBatch={
                        'Changes': records_to_delete
                    }
                )
                print("Records deleted, waiting for changes to propagate...")
                # Optionally wait or check change status here

            # Finally, delete the hosted zone
            print(f"Deleting hosted zone {hosted_zone_id}...")
            client.delete_hosted_zone(Id=hosted_zone_id)
            print(f"Hosted zone {hosted_zone_id} deleted successfully.")

        except ClientError as e:
            print(f"Error deleting hosted zone {hosted_zone_id}: {e}")

        return