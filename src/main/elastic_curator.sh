#!/bin/bash

export LC_ALL=en_US.utf8
curator --config /home/ubuntu/happening/src/main/CONFIGURATION_FILE.yml --dry-run /home/ubuntu/happening/src/main/ACTION_FILE.yml 
