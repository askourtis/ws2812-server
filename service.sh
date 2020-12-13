#!/bin/bash

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
NAME=smart-leds-server
CONTENTS="[Unit]
Description=Smart Leds DIY Server
Wants=network-online.target
After=network-online.target

[Service]
Type=forking
RemainAfterExit=yes
WorkingDirectory=$HOME_DIR
ExecStart=$HOME_DIR/start.sh
ExecStop=$HOME_DIR/stop.sh

[Install]
WantedBy=multi-user.target"


echo "[Service $NAME]"
echo "Stopping service..."
systemctl stop $NAME
echo "Disabling service..."
systemctl disable $NAME
echo "Installing service..."
echo -e "$CONTENTS" > /etc/systemd/system/$NAME.service
echo "Reloading..."
systemctl daemon-reload
echo "Enabling service..."
systemctl enable $NAME
echo "Starting service..."
systemctl start $NAME
echo "Done."
