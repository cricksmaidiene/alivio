#!/bin/bash
set -e

# Define private repositories URLs
ALIVIO_GITH=github.com/cricksmaidiene/alivio.git

# Define directory to clone repositories
BASE_WORK_DIR=/databricks/repo

# pip install --upgrade pip
pip install poetry awscli chardet

# Clone the repositories
git clone https://$GITHUB_TOKEN:@$ALIVIO_GITH $BASE_WORK_DIR/alivio --depth 1


cd $BASE_WORK_DIR/alivio
poetry install --no-root

# For databricks runtime 13.3 LTS
pip install virtualenv==20.16.3