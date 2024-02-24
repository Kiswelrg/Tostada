from importlib import import_module
import inspect
from typing import get_type_hints


# Usage
# module_path = 'user.views'
# function_name = 'Home'
# my_function = import_function(module_path, function_name)
def importFunction(module_path, function_name):
    module = import_module(module_path)
    return getattr(module, function_name)



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
