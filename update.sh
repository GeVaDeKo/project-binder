#!/bin/bash

set -e

INSTALL_DIR="/opt/project-binder"

echo "Updating Project Binder..."

cd "$INSTALL_DIR"

sudo git pull

echo "Done!"