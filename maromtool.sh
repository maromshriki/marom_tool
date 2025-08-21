#!/bin/bash

echo "Making sure everything is ready..."


sudo yum update -y


sudo yum install -y python3


sudo yum install -y python3-pip

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

unzip awscliv2.zip

sudo ./aws/install
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not available. Something went wrong."
    exit 1
fi


echo "Installing Python requirements..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "There was a problem installing the requirements."
    exit 1
fi


echo "You can use the tool now. Running it..."
python3 tool.py

