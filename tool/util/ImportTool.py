from importlib import import_module
import importlib.util
import inspect
from typing import get_type_hints
import os

# Usage
# module_path = 'user.views'
# function_name = 'Home'
# my_function = import_function(module_path, function_name)
def importFunction(module_path, function_name):
    module = import_module(module_path.replace('/', '.'))
    return getattr(module, function_name)



def import_function_from_file(file_path, function_name):
    print(file_path, function_name)
    print(os.getcwd())
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


def importTest(server_code, tool_code, function_name):
    # Specify the path to somefunctionsinhere.py
    file_path = "dir_A/dir_B/somefunctionsinhere.py"
    # Specify the name of the function you want to import
    function_name = "some_function"

    # Import the function dynamically
    return import_function_from_file(file_path, function_name)



# Get the signature of the function
def getParamsAndReturn(function):
    signature = inspect.signature(function)

    # Get the input arguments and types
    input_args = {}
    for param in signature.parameters.values():
        input_args[param.name] = param.annotation

    # Get the return type
    return_type = signature.return_annotation

    # Print the results
    return [input_args, return_type]
