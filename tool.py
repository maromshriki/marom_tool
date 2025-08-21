import argparse
from ec2_handler import handle_ec2
from s3_handler import handle_s3
from route53_handler import handle_route53

def main():
    parser = argparse.ArgumentParser(description="Platform CLI for AWS resource provisioning")
    parser.add_argument("resource", choices=["ec2", "s3", "route53"], help="Resource type")
    parser.add_argument("action", choices=["create", "start", "stop", "update", "delete", "list"], help="Action to perform")
    parser.add_argument("--params", nargs="*", help="Key=Value parameters")

    args = parser.parse_args()
    param_dict = dict(p.split("=", 1) for p in args.params) if args.params else {}

    if args.resource == "ec2":
        handle_ec2(args.action, param_dict)
    elif args.resource == "s3":
        handle_s3(args.action, param_dict)
    elif args.resource == "route53":
        handle_route53(args.action, param_dict)

if __name__ == "__main__":
    main()
