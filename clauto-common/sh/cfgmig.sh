#!/bin/bash

# This script compares an existing Clauto module config
# file to a cfgtemplate.txt file and updates
# the Clauto module config with every setting from
# template.cfg that it doesn't have yet

CFG_FILE=/etc/clauto/$1/$1.cfg
TEMPLATE_FILE=/usr/share/clauto/$1/cfgmig/template.cfg

# If the config file doesn't exist, create a blank one
if [ ! -f $CFG_FILE ] ; then
    touch $CFG_FILE
    echo "# Configuration file for $1" > $CFG_FILE
    echo "[cfgmig] Created $1.cfg"
fi

# Prepare a flag to determine whether to inform the user of changes
cfg_changed=0

# Iterate through each line in template.cfg.
# The IFS and echo are a trick to add a trailing newline to template.cfg so that the read command won't get stuck on the last line
# The parenthesis before "while" is matched near the end of the script. It puts the IF-statements at the end in the same subshell
# as the loop so that the value of cfg_changed will carry over isntead of being wiped out when the subshell dies
IFS=
echo "$(cat $TEMPLATE_FILE)" | ( while read line ; do
    # Only consider lines with settings - no comments
    if [[ $line =~ ^[[:space:]]*[A-Za-z0-9]([A-Za-z0-9_]*[A-Za-z0-9])?[[:space:]]*=.*$ ]] ; then
        # Pull out the key
        key=$(echo "$line" | sed -r -e 's/=.*$//g')

        # If the key isn't in the Clauto module config, then add the line
        if [ "$(cat $CFG_FILE | egrep ^\\s*$key\\s*=.*$)" == "" ] ; then
            echo $line >> $CFG_FILE
            cfg_changed=1
        fi
    fi
done

# If something changed, let the user know
if [ $cfg_changed -eq 1 ]; then
    echo "[cfgmig] Added new lines to $CFG_FILE"
    exit 0
else
    echo "[cfgmig] $CFG_FILE unchanged"
    exit 0
fi )