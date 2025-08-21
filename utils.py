import os
import getpass

def get_username():
    return os.getenv("USER") or getpass.getuser()

def resource_tagged_by_cli(tags):
    return any(tag['Key'] == 'CreatedBy' and tag['Value'] == 'platform-cli' for tag in tags)

def confirm_public_bucket():
    response = input("Are you sure you want to create a public bucket? (yes/no): ")
    return response.lower() == "yes"

def get_latest_ami(os_choice):
    # For brevity, hardcoded AMI IDs (you'd ideally query or cache latest IDs)
    if os_choice == "ubuntu":
        return "ami-0abcdef1234567890"  # Update with latest Ubuntu AMI ID
    return "ami-0fedcba9876543210"  # Update with latest Amazon Linux AMI ID
