#!/bin/bash

export WORK_DIR=${1}
export INITIAL_PROJECT_LOCATION=${2}
export SHARED_API_DIR=${3}
export RRD_DATA_STORAGE_DIR=${4}/api.pmccabe_collector.restapi.org

export PYTHONPATH="${WORK_DIR}:${WORK_DIR}/utils:${WORK_DIR}/utils/modules"
UTILS="${WORK_DIR}/utils"
export MODULES="${WORK_DIR}/utils/modules"

export MAIN_SERVICE_NAME=api.pmccabe_collector.restapi.org

rm -rf ${RRD_DATA_STORAGE_DIR}
mkdir -p ${RRD_DATA_STORAGE_DIR}

# inject test files into project directory
test_files=(/package/test_data/*.cpp)
for f in ${test_files[@]}; do
    cp ${f} ${INITIAL_PROJECT_LOCATION}/
done
echo "Create CC API which RRD depends on"
${UTILS}/build_api_pseudo_fs.py /cc_API ${SHARED_API_DIR}
echo "Mock CC API for standalone functional tests only"
rm -f ${SHARED_API_DIR}/${MAIN_SERVICE_NAME}/cc/statistic/GET/result.xml_fake_data
fake_statistic_data_result=${SHARED_API_DIR}/${MAIN_SERVICE_NAME}/cc/statistic/GET/result.xml_fake_data
find ${INITIAL_PROJECT_LOCATION} -regex ".*\\.\\(hpp\\|cpp\\|c\\|h\\)" -type f | /package/pmccabe_visualizer/pmccabe_build.py > ${fake_statistic_data_result}
real_statistic_pipe_out=${SHARED_API_DIR}/${MAIN_SERVICE_NAME}/cc/statistic/GET/result.xml_${RRD_TESTABLE_CONTAINER_HOSTNAME}
if [ -e ${real_statistic_pipe_out} ]; then
    rm -f ${real_statistic_pipe_out}
fi
mkfifo -m 644 ${real_statistic_pipe_out}
echo 0 > ${SHARED_API_DIR}/${MAIN_SERVICE_NAME}/cc/statistic/GET/exec
(
while :
do
    echo "`date +%H:%M:%S:%3N`    START:`cat ${SHARED_API_DIR}/${MAIN_SERVICE_NAME}/cc/statistic/GET/exec`"
    echo "`date +%H:%M:%S:%3N`    MOCK FINISH: ${real_statistic_pipe_out}"
    cat ${fake_statistic_data_result} > ${real_statistic_pipe_out}
    echo "`date +%H:%M:%S:%3N`    MOCK CONSUMED: ${real_statistic_pipe_out}"
done
) &
WATCH_PID=$!
cat ${real_statistic_pipe_out}

echo "Run tests:"
RET=0
for s in ${WORK_DIR}/test_*.py; do
    # '-s' argument repeals console output capturing by pytest, which allow us
    # to use heartbeat mechanism to keep `test_aggregator` alive during
    # long test cases execution (likewise RRDs collecting)
    pytest -s ${s}
    VAL=$?
    if [ $VAL != 0 ]
    then
        RET=$VAL
    fi
done

# remove test files from project directory
for f in ${test_files[@]}; do
    fname=`basename ${f}`
    rm -f ${INITIAL_PROJECT_LOCATION}/${fname}
done

kill -15 ${WATCH_PID}
wait ${WATCH_PID}
if [ $EXIT_ONCE_DONE == true ]; then exit $RET; fi

echo "wait for termination"
sleep infinity &
wait $!
exit $RET
