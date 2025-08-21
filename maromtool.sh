#!/usr/bin/env bash



set -e

echo " Setting up marom_tool"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    if command -v yum &> /dev/null; then
        sudo yum update -y
        sudo yum install -y python3
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update -y
        sudo apt-get install -y python3 python3-venv python3-pip
    else
        echo "❌ Package manager not found (yum/apt-get). Install Python3 manually."
        exit 1
    fi
fi

# ---------- בדיקה/התקנה של pip ----------
if ! command -v pip3 &> /dev/null; then
    echo " pip3 not found. Installing..."
    if command -v yum &> /dev/null; then
        sudo yum install -y python3-pip
    elif command -v apt-get &> /dev/null; then
        sudo apt-get install -y python3-pip
    fi
fi

# ---------- יצירת venv ----------
if [ ! -d "venv" ]; then
    echo " Creating virtual environment..."
    python3 -m venv venv
fi

# הפעלת venv
source venv/bin/activate

# ---------- התקנת דרישות ----------
if [ -f "requirements.txt" ]; then
    echo " Installing dependencies..."
    pip install -r requirements.txt
else
    echo "⚠ No requirements.txt found. Installing boto3 by default..."
    pip install boto3
fi


python3 tool.py "$@"

