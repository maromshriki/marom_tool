 #!/usr/bin/env bash

echo " Setting up marom_tool.." 



sudo yum update -y
sudo yum install -y python3
sudo yum install -y python3-pip
echo " Installing dependencies..."
pip install -r requirements.txt

python3 tool.py 
