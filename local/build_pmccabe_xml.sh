#!/bin/bash

. ${1}/setenv.sh

XML_NAME=${2}
find ${INITIAL_PROJECT_LOCATION} -regex ".*\.\(hpp\|cpp\|c\|h\)" | grep -v "buil" | grep -v "3pp" | grep -v "thirdpart" | ${WORK_DIR}/pmccabe_visualizer/pmccabe_build.py > ${XML_NAME}
