marom_tool

A simple CLI tool for managing AWS resources (EC2, S3, Route53).

📦 Prerequisites

Before installing and running the tool, make sure your environment is ready:

AWS CLI installed:
run:

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install


AWS credentials configured (required):

Run:

aws configure


Enter your Access Key, Secret Key, Region


git and Python 3 installed.




Clone the repository and prepare the CLI:

git clone https://github.com/your-org/marom_tool.git
cd marom_tool
chmod +x maromtool



Run commands using the maromtool script:

EC2
./maromtool ec2 list
./maromtool ec2 start --params instance_id=i-0123456789abcdef
./maromtool ec2 stop --params instance_id=i-0123456789abcdef
./maromtool ec2 delete --params instance_id=i-0123456789abcdef

S3
./maromtool s3 list
./maromtool s3 create --params bucket_name=my-bucket
./maromtool s3 delete --params bucket_name=my-bucket

Route53
./maromtool route53 list
./maromtool route53 create --params zone_name=example.com record_name=www.example.com record_type=A record_value=1.2.3.4
./maromtool route53 delete --params record_name=www.example.com record_type=A

📂 Project Structure

tool.py – Main CLI entrypoint (argument parser)

ec2_handler.py – EC2 operations

s3_handler.py – S3 operations

route53_handler.py – Route53 operations

maromtool – Startup script (sets up virtualenv and runs the CLI)

requirements.txt – Python dependencies (e.g., boto3)

🛡️ Notes

The tool requires valid AWS IAM permissions to manage resources.

Destructive actions (delete) are irreversible – make sure to specify the correct IDs or names.

If no requirements.txt is found, the script installs boto3 by default.




