import inspect
from typing import Callable
from collections import namedtuple

class PublicMethod:
    """
    This class accepts a method and provides a handy interface to execute it and validate command before the execution.
    Commands looks like: {"function": "method_name", "parameter1": "some string", "parameter2": 5 ...}
    """
    def __init__(self, method: Callable):
        self.name = method.__name__
        self.docs = method.__doc__ or "No documentation provided."
        self.method = method
        self.annotations = self.method.__annotations__
        self.params = self._get_parameters_data()

    def __call__(self, command: dict):
        command.pop("function")
        if command.keys() >= set(self.params["mandatory"]):
            return self.method(**command)
        raise ValueError(f"Mandatory parameters for command {self.name} are: {self.params['mandatory']}. Optional parameters: {self.params['optional']}")

    def __repr__(self):
        return f"Method: {self.name},\n parameters: {self.params},\n docs: {self.docs}\n"

    def _get_parameters_data(self):
        full_arg_spec = inspect.getfullargspec(self.method)
        output_dict = {}
        try:
            full_arg_spec.args.remove("self")
        except ValueError:
            pass
        if full_arg_spec.defaults:
            output_dict["mandatory"] = {arg_name: self.annotations.get(arg_name, any).__name__ for arg_name in full_arg_spec.args[:-len(full_arg_spec.defaults)]}
            output_dict["optional"] = {arg_name: self.annotations.get(arg_name, any).__name__ for arg_name in full_arg_spec.args[-len(full_arg_spec.defaults):]}
        else:
            output_dict["mandatory"] = {arg_name: self.annotations.get(arg_name, any).__name__ for arg_name in full_arg_spec.args}
            output_dict["optional"] = list() ## TODO: This should be an empty dict
        return output_dict

    def get_dict_for_web(self):
        return {'name': self.name, 'docs': self.docs.replace('\n', '<br>'), 'params': self.params}

    def validate_command(self, command: dict, with_types: bool = False) -> tuple[bool, dict, str]:
        ValidatedCommand = namedtuple("ValidatedCommand", ["is_valid", "converted", "errors"])
        is_valid: bool = True
        errors: str = ""
        converted_command = {**command}
        if not command.keys() >= set(self.params["mandatory"]):
            is_valid = False
            errors += f"Mandatory parameters for command {self.name} are: {self.params['mandatory']}. Optional parameters: {self.params['optional']}\n"
        if with_types:
            for name, param in command.items():
                if (type_:= self.annotations.get(name)) is not None:
                    try:
                        converted_command[name] = type_(param)
                    except ValueError as ex:
                        is_valid = False
                        errors += f"Error for parameter {name}: " + repr(ex) + "\n"
        return ValidatedCommand(is_valid, converted_command, errors)
