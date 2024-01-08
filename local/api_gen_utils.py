#!/usr/bin/python

import os
import stat

def get_generated_scripts_path():
    return "services"


def get_api_hidden_node_name():
    return ".hid"


def compose_api_gui_service_script_name(req_name):
    return f"{req_name}_listener.sh"

def compose_api_cli_service_script_name(req_name):
    return f"{req_name}_server.sh"

def get_api_gui_service_script_path(req_name):
        return os.path.join(
            get_generated_scripts_path(), compose_api_gui_service_script_name(req_name)
        )

def get_api_cli_service_script_path(req_name):
        return os.path.join(
            get_generated_scripts_path(), compose_api_cli_service_script_name(req_name)
        )

def compose_api_exec_script_name(script_name):
    return f"{script_name}_exec.sh"


def append_file_mode(file, append_modes):
    st = os.stat(file)
    os.chmod(file, st.st_mode | append_modes)

def append_file_list_mode(file_list, append_modes):
    for f in file_list:
        append_file_mode(f, append_modes)


def make_file_executable(file):
    append_file_mode(file, stat.S_IEXEC)


def compose_api_help_script_name(script_name):
    return f"{script_name}_help.sh"


def compose_api_fs_node_name(api_root, req, rtype):
    anode = os.path.join(api_root, req)
    areq_node = os.path.join(anode, rtype)
    return anode, areq_node
