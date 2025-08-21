#!/usr/bin/env python3
import argparse
from ec2_handler import handle_ec2
from s3_handler import handle_s3
from route53_handler import handle_route53

def main():
    parser = argparse.ArgumentParser(
        description="AWS CLI tool for EC2, S3, and Route53"
    )

    subparsers = parser.add_subparsers(dest="resource", required=True)

    # ----------------- EC2 -----------------
    ec2_parser = subparsers.add_parser("ec2", help="Manage EC2 instances")
    ec2_sub = ec2_parser.add_subparsers(dest="action", required=True)

    # EC2 create
    ec2_create = ec2_sub.add_parser("create", help="Create an EC2 instance")
    ec2_create.add_argument("--type", dest="instance_type", default="t3.micro")

    # EC2 delete
    ec2_delete = ec2_sub.add_parser("delete", help="Delete EC2 instance(s)")
    ec2_delete.add_argument("--id", dest="instance_id", help="Instance ID to delete")
    ec2_delete.add_argument("--all-tagged", action="store_true",
                            help="Delete all instances tagged with CreatedBy=platform-cli")
    ec2_delete.add_argument("--yes", action="store_true",
                            help="Skip confirmation for multiple deletions")
    ec2_delete.add_argument("--dry-run", action="store_true", help="Show what would happen")

    # EC2 list
    ec2_sub.add_parser("list", help="List EC2 instances")

    # ----------------- S3 -----------------
    s3_parser = subparsers.add_parser("s3", help="Manage S3 buckets")
    s3_sub = s3_parser.add_subparsers(dest="action", required=True)

    # S3 create
    s3_create = s3_sub.add_parser("create", help="Create an S3 bucket")
    s3_create.add_argument("--name", dest="bucket_name", required=True)

    # S3 delete
    s3_delete = s3_sub.add_parser("delete", help="Delete an S3 bucket")
    s3_delete.add_argument("--name", dest="bucket_name", required=True)
    s3_delete.add_argument("--yes", action="store_true", help="Force delete non-empty bucket")
    s3_delete.add_argument("--dry-run", action="store_true", help="Show what would happen")

    # S3 list
    s3_sub.add_parser("list", help="List S3 buckets")

    # ----------------- Route53 -----------------
    r53_parser = subparsers.add_parser("route53", help="Manage Route53 hosted zones")
    r53_sub = r53_parser.add_subparsers(dest="action", required=True)

    # Route53 create
    r53_create = r53_sub.add_parser("create", help="Create a hosted zone")
    r53_create.add_argument("--domain", dest="domain_name", required=True)

    # Route53 delete
    r53_delete = r53_sub.add_parser("delete", help="Delete a hosted zone")
    r53_delete.add_argument("--id", dest="hosted_zone_id", required=True)
    r53_delete.add_argument("--yes", action="store_true", help="Force delete records inside zone")
    r53_delete.add_argument("--dry-run", action="store_true", help="Show what would happen")

    # Route53 list
    r53_sub.add_parser("list", help="List hosted zones")

    args = parser.parse_args()

    # הפעלת handler לפי resource
    params = vars(args)  # המרה ל-dict
    if args.resource == "ec2":
        handle_ec2(args.action, params)
    elif args.resource == "s3":
        handle_s3(args.action, params)
    elif args.resource == "route53":
        handle_route53(args.action, params)

if __name__ == "__main__":
    main()

