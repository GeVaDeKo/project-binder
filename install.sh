#!/bin/bash

set -e

REPO="https://github.com/GeVaDeKo/project-binder.git"
INSTALL_DIR="/opt/project-binder"

echo "================================="
echo " Project Binder Installer"
echo "================================="
echo

echo "Downloading..."

sudo rm -rf "$INSTALL_DIR"

sudo git clone "$REPO" "$INSTALL_DIR"

sudo chmod +x "$INSTALL_DIR/project-binder.py"

sudo ln -sf "$INSTALL_DIR/project-binder.py" /usr/local/bin/binder

echo
echo "Project Binder installed successfully!"
echo
echo "Try:"
echo
echo "binder /path/to/project"