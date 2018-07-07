#!/bin/bash

# This script copies the clauto_common Python module in the repo
# into /opt/venv/... where it replaces the local installation of
# the module. It's a way of testing new code without doing a release

# Ensure clauto-common is installed
if [ "$(dpkg-query -W --showformat='${Status}\n' clauto-common | grep 'install ok installed')" == "" ] ; then
    echo "[deplocal] clauto-common not installed"
    exit 1
fi

# Copy the clauto_common source from the repo to the clautod installation directory
sudo cp -r clauto_common/* /opt/venvs/clauto-common/lib/python3.5/site-packages/clauto_common