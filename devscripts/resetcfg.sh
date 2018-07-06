#!/bin/bash

# This script resets the config of the local
# instance of a Clauto service, as if it was
# just installed for the first time

# Ensure the Clauto service is installed
if [ "$(dpkg-query -W --showformat='${Status}\n' $1 | grep 'install ok installed')" == "" ] ; then
    echo "[resetcfg] $1 not installed"
    exit 1
fi

# Bring down the clauto service instance
echo "[resetcfg] Stopping $1..."
sudo systemctl stop $1

# Delete the config
echo "[resetcfg] $1 stopped. Deleting config..."
sudo rm -f /etc/clauto/$1/$1.cfg

# Enact config migration to rebuild the config
echo "[resetcfg] Config deleted. Enacting config migration..."
sudo /usr/share/clauto/clauto-common/sh/cfgmig.sh $1

# Bring up the Clauto service instance
echo "[resetcfg] Config migration complete. Starting $1..."
sudo systemctl start $1

echo "[resetcfg] $1 started."
echo "[resetcfg] State reset."