#!/usr/bin/python

import api_fs_exec_utils

def make_script_analytic(script, desired_file_ext=""):
    if len(desired_file_ext) == 0:
        file_extension = ""
    else:
        file_extension = "." + desired_file_ext

    body = (
        *api_fs_exec_utils.generate_exec_header(), r"",
        *api_fs_exec_utils.generate_get_result_type(file_extension), r"",
        *api_fs_exec_utils.generate_api_node_env_init(), r"",
        *api_fs_exec_utils.generate_read_api_fs_args(), r"",
        r'echo "${brr[@]}"',
    )
    script.writelines(line + "\n" for line in body)

def generate_script_analytic_help():
    return "rrdtool -h"

def make_script_rrd(script, desired_file_ext=""):
    if len(desired_file_ext) == 0:
        file_extension = ""
    else:
        file_extension = "." + desired_file_ext

    body = (
        *api_fs_exec_utils.generate_exec_header(), r"",
        *api_fs_exec_utils.generate_get_result_type(file_extension), r"",
        *api_fs_exec_utils.generate_api_node_env_init(), r"",
        *api_fs_exec_utils.generate_read_api_fs_args(), r"",
        r'echo "${brr[@]}"',
    )
    script.writelines(line + "\n" for line in body)

def generate_script_rrd_help():
    return "rrdtool -h"

def make_script_rrd_collect(script, desired_file_ext=""):
    if len(desired_file_ext) == 0:
        file_extension = ""
    else:
        file_extension = "." + desired_file_ext

    body = (
        *api_fs_exec_utils.generate_exec_header(), r"",
        *api_fs_exec_utils.generate_get_result_type(file_extension), r"",
        *api_fs_exec_utils.generate_api_node_env_init(), r"",
        *api_fs_exec_utils.generate_bypassed_params_formatting(), r"",
        *api_fs_exec_utils.generate_read_api_fs_args(), r"",
        r'echo ${IN_ARGS[@]} > ${SHARED_API_DIR}/cc/analytic/rrd/PUT/exec',
        r'RRD_DB_PARAMS=`cat ${SHARED_API_DIR}/cc/analytic/rrd/PUT/result`',
        r'echo 0 > ${SHARED_API_DIR}/cc/analytic/PUT/exec',
        r'ONLY_METRICS_IN_RANGE=`cat ${SHARED_API_DIR}/cc/analytic/PUT/result`',
        r'echo $(replace_space_in_even_position "${ONLY_METRICS_IN_RANGE}") > ${SHARED_API_DIR}/cc/statistic/GET/exec',
        r'cat ${SHARED_API_DIR}/cc/statistic/GET/result.xml | ${WORK_DIR}/build_rrd.py "${RRD_DB_PARAMS}" ${SHARED_API_DIR} ${brr[@]}',
    )
    script.writelines(line + "\n" for line in body)

def generate_script_rrd_collect_help():
    return "rrdtool -h"

def make_script_rrd_select(script, desired_file_ext=""):
    if len(desired_file_ext) == 0:
        file_extension = ".txt"
    else:
        file_extension = "." + desired_file_ext
    body = (
        *api_fs_exec_utils.generate_exec_header(), r"",
        *api_fs_exec_utils.generate_get_result_type(file_extension), r"",
        *api_fs_exec_utils.generate_api_node_env_init(), r"",
        *api_fs_exec_utils.generate_read_api_fs_args(), r"",
        r'echo "${brr[@]}" | xargs find ${RRD_ROOT}',
    )
    script.writelines(line + "\n" for line in body)

def generate_script_rrd_select_help():
    return "rrdtool -h"

def make_script_rrd_view(script, desired_file_ext=""):
    if len(desired_file_ext) == 0:
        file_extension = ".csv"
    else:
        file_extension = "." + desired_file_ext
    body = (
        *api_fs_exec_utils.generate_exec_header(), r"",
        *api_fs_exec_utils.generate_get_result_type(file_extension), r"",
        *api_fs_exec_utils.generate_api_node_env_init(), r"",
        r'echo "${IN_ARGS[@]}" > ${SHARED_API_DIR}/cc/analytic/rrd/select/GET/exec',
        r'cat ${SHARED_API_DIR}/cc/analytic/rrd/select/GET/result.txt | ${WORK_DIR}/fetch_rrd.py ${SHARED_API_DIR}/cc/analytic/rrd/select/view',
    )
    script.writelines(line + "\n" for line in body)

def generate_script_rrd_view_help():
    return "rrdtool -h"

def make_script_rrd_plot_view(script, desired_file_ext=""):
    if len(desired_file_ext) == 0:
        file_extension = ".png"
    else:
        file_extension = "." + desired_file_ext

    body = (
        *api_fs_exec_utils.generate_exec_header(), r"",
        *api_fs_exec_utils.generate_get_result_type(file_extension), r"",
        *api_fs_exec_utils.generate_api_node_env_init(), r"",
        r"RESULT_FILE=`mktemp -u`",
        r'echo "${IN_ARGS[@]}" > ${SHARED_API_DIR}/cc/analytic/rrd/select/GET/exec',
        r'cat ${SHARED_API_DIR}/cc/analytic/rrd/select/GET/result.txt | ${WORK_DIR}/graph_rrd.py ${SHARED_API_DIR}/cc/analytic/rrd/select/plot_view ${RESULT_FILE}',
        r'cat ${RESULT_FILE}.png',
        r'rm -f ${RESULT_FILE}.png'
    )

    script.writelines(line + "\n" for line in body)

def generate_script_rrd_plot_view_help():
    return "rrdtool -h"



def get():
    scripts_generator = {
        "analytic": make_script_analytic,
        "rrd": make_script_rrd,
        "rrd_collect": make_script_rrd_collect,
        "rrd_select": make_script_rrd_select,
        "rrd_view": make_script_rrd_view,
        "rrd_plot_view": make_script_rrd_plot_view
    }

    scripts_help_generator = {
        "analytic": generate_script_analytic_help,
        "rrd": generate_script_rrd_help,
        "rrd_collect": generate_script_rrd_collect_help,
        "rrd_select": generate_script_rrd_select_help,
        "rrd_view": generate_script_rrd_view_help,
        "rrd_plot_view": generate_script_rrd_plot_view_help
    }
    return scripts_generator, scripts_help_generator
