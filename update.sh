#!/bin/bash

set -e

INSTALL_DIR="/opt/project-binder"
BIN_LINK="/usr/local/bin/binder"

echo "Updating Project Binder..."

if [ ! -d "$INSTALL_DIR/.git" ]; then
    echo "Project Binder is niet geïnstalleerd via git in $INSTALL_DIR"
    exit 1
fi

cd "$INSTALL_DIR"

sudo git pull origin main

sudo chmod +x "$INSTALL_DIR/project-binder.py"
sudo ln -sf "$INSTALL_DIR/project-binder.py" "$BIN_LINK"

echo "Project Binder updated successfully!"
echo
echo "Try:"
echo "binder --help"