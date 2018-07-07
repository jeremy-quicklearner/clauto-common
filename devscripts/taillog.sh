#!/bin/bash

CFG_FILE=/etc/clauto/$1/$1.cfg
CFG_KEY_LOG_DIR=log_dir

# First, determine the log's location by reading the config file. Filter out the line with the log's location
log_dir=$(cat $CFG_FILE | egrep ^\\s*$CFG_KEY_LOG_DIR\\s*=.*$)

# Trim off the key and '=' character
log_dir=$(echo $log_dir | sed -r -e 's/.*=\s*//g')

# Trim off any trailing whitespace or comment
log_dir=$(echo $log_dir | sed -r -e 's/\s*(#.*)?//g')

# Now the absolute path of the database is known
log_file=$log_dir/$1.log

# Set up an escape character for sed
esc=$(printf '\033')

# Now tail the log and add fancy colours
# This incredibly ugly pile of regex and ANSI escape characters is here and not in Python because the actual log
# file should be straightforward uncoloured ASCII - not something weird and colourful that might trip up parsers
# Also, I'm sorry to anyone who ever feels the need to edit this
unbuffer tail -f $log_file | sed "
     s/\[CRT\].*/${esc}[31m\0${esc}[39m/g;
     s/\[CFG\]/${esc}[36;1m\0${esc}[39;0m/g;
     s/\[ERR\].*/${esc}[33;1m\0${esc}[39;0m/g;
     s/\[WRN\].*/${esc}[33m\0${esc}[39m/g;
     s/\[INF\]/${esc}[32m\0${esc}[39m/g;
     s/\[DBG\].*/${esc}[34;1m\0${esc}[39;0m/g;
     s/\[VRB\].*/${esc}[35;1m\0${esc}[39;0m/g;
     s/\[DBG\]\[\(.*\)\]\(.*\)/${esc}[35m[DBG][${esc}[36m\1${esc}[35m]\2${esc}[39m/g;
     s/\[VRB\]\[\(.*\)\]\(.*\)/${esc}[34m[VRB][${esc}[36m\1${esc}[34m]\2${esc}[39m/g;
     s/${esc}\[31m\(.*\)<\([^><]\)>/${esc}[31m\1<${esc}[36;1m\2${esc}[31;0m${esc}[31m>/g;
     s/${esc}\[31m\([^><]*\)<\([^><]\)>/${esc}[31m\1<${esc}[36;1m\2${esc}[31;0m${esc}[31m>/g;
     s/${esc}\[39m\(.*\)<\([^><]\)>/${esc}[39m\1<${esc}[36;1m\2${esc}[39;0m${esc}[39m>/g;
     s/${esc}\[39m\([^><]*\)<\([^><]\)>/${esc}[39m\1<${esc}[36;1m\2${esc}[39;0m${esc}[39m>/g;
     s/${esc}\[39;0m\(.*\)<\([^><]\)>/${esc}[39;0m\1<${esc}[36;1m\2${esc}[39;0m${esc}[39m>/g;
     s/${esc}\[39;0m\([^><]*\)<\([^><]\)>/${esc}[39;0m\1<${esc}[36;1m\2${esc}[39;0m${esc}[39m>/g;
     s/${esc}\[33m\(.*\)<\([^><]\)>/${esc}[33m\1<${esc}[36;1m\2${esc}[33;0m${esc}[33m>/g;
     s/${esc}\[33m\([^><]*\)<\([^><]\)>/${esc}[33m\1<${esc}[36;1m\2${esc}[33;0m${esc}[33m>/g;
     s/${esc}\[33;1m\(.*\)<\([^><]\)>/${esc}[33;1m\1<${esc}[36m\2${esc}[33m${esc}[33m>/g;
     s/${esc}\[33;1m\([^><]*\)<\([^><]\)>/${esc}[33;1m\1<${esc}[36m\2${esc}[33m${esc}[33m>/g;
     s/${esc}\[34m\(.*\)<\([^><]\)>/${esc}[34m\1<${esc}[36;1m\2${esc}[34m${esc}[34m>/g;
     s/${esc}\[34m\([^><]*\)<\([^><]\)>/${esc}[34m\1<${esc}[36;1m\2${esc}[34m${esc}[34m>/g;
     s/${esc}\[35m\(.*\)<\([^><]\)>/${esc}[35m\1<${esc}[36;1m\2${esc}[35m${esc}[35m>/g;
     s/${esc}\[35m\([^><]*\)<\([^><]\)>/${esc}[35m\1<${esc}[36;1m\2${esc}[35m${esc}[35m>/g;
"