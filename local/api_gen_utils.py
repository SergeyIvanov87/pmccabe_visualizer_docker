#!/usr/bin/python

import json
import os
import stat
import filesystem_utils

def get_generated_scripts_path():
    return "services"


def get_api_hidden_node_name():
    return ".hid"

def get_api_leaf_node_name(req_type):
    leaf_names = {"GET": get_api_hidden_node_name(), "PUT": "modify_this_file", "POST": "modify_this_file"}
    if req_type not in leaf_names.keys():
        print("Unsupported req_type: {req_type}. Default leaf node will be generated: api_file")
        return "api_file"
    return leaf_names[req_type]

def compose_api_gui_service_script_name(req_name):
    return f"{req_name}_listener.sh"

def compose_api_cli_service_script_name(req_name):
    return f"{req_name}_server.sh"

def get_api_gui_service_script_path(api_server_scripts_path_dir, req_name):
        return os.path.join(
            api_server_scripts_path_dir, compose_api_gui_service_script_name(req_name)
        )

def get_api_cli_service_script_path(api_server_scripts_path_dir, req_name):
        return os.path.join(
            api_server_scripts_path_dir, compose_api_cli_service_script_name(req_name)
        )

def compose_api_exec_script_name(script_name):
    return f"{script_name}_exec.sh"

def compose_api_help_script_name(script_name):
    return f"{script_name}_help.sh"


def compose_api_fs_node_name(api_root, req, rtype):
    anode = os.path.join(api_root, req)
    areq_node = os.path.join(anode, rtype)
    return anode, areq_node



def get_api_schema_files(root_directory):
    directory_str = os.fsdecode(root_directory)
    return [os.path.join(directory_str, os.fsdecode(file)) for file in os.listdir(root_directory) if os.fsdecode(file).endswith(".json")]

def decode_api_request_from_schema_file(api_request_schema_path):
    must_have_fields=["Method", "Query", "Params"]
    request = ""
    name = ""
    with open(api_request_schema_path, "r") as file:
        try:
            request = json.load(file)
            for f in must_have_fields:
                if f not in request:
                    raise ValueError(f"API schema must describe attribute: {f}. Check the schema in: {api_request_schema_path}")
            name = os.path.basename(api_request_schema_path).split('.')[0]
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"Error: {str(e)} in file: {api_request_schema_path}")
    return name, request

def get_api_request_plain_params(req_param_json):
    params_list = []
    for p in req_param_json:
        # access only plain data
        if isinstance(req_param_json[p], str):
            params_list.append(str(p) + "=" + req_param_json[p])
    return params_list
