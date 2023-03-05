from PublicMethod import PublicMethod

class ExampleClass:
    def __init__(self) -> None:
        self.some_value = 'instance attribute'
        self.public_methods = self._get_public_methods()

    def _get_public_methods(self):
        public_methods: dict[str, PublicMethod] = {func: PublicMethod(getattr(self, func)) for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_") and not func in ("execute_command_old", "execute_command", "get_public_methods")}
        return public_methods

    @classmethod
    def get_public_methods(cls):
        public_methods: dict[str, PublicMethod] = {func: PublicMethod(getattr(cls, func)) for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith("_") and not func in ("execute_command_old", "execute_command", "get_public_methods")}
        return public_methods

    def execute_command(self, command: dict):
        try:
            if command.get("function") is None:
                raise ValueError("Command needs to have 'function' key")
            if (method := self.public_methods.get(command["function"])) is None:
                raise NotImplementedError(f"Function {command['function']} is not implemented yet")
            result = method(command)
            return {"status": 0, "error": "", "result": result if result is not None else ""}
        except NotImplementedError as ex:
            print(repr(ex))
            return [-4000, "not implemented" , repr(ex)]
        except Exception as ex:
            # Write exception to DB etc.
            print(repr(ex))
            return [-1, "something went wrong", repr(ex)]

    def complex_public_method(self, a: int, b: str, c: str = "default_value"):
        """ Documentation of a public method. This method does something cool.

        Args:
            a (int): Integer for operations
            b (str): Integer for operations
            c (str, optional): Optional parameter. Defaults to "default_value".
        """
        print(a, b, c)
        return "successfully executed complex_public_method"
        # Many lines of complicated code, which may throw some exceptions
        # Note that try except block is not used, because the exceptions are catched in `PublicMethod.execute()` method

    def simple_public_method(self, x: int, y):
        # No docstring for this function. Also, no optional parameters and not fully typed.
        print(x, y, self.some_value)
        return "successfully executed simple_public_method"

    def _private(self, a: str) -> None:
        """
        This method has underscore at the beginning of its name so it will not appear in instance attribute `self.public_methods`
        """
        pass


if __name__ == "__main__":
    t = ExampleClass()
    print(t.public_methods['complex_public_method'].validate_command({"a": "5", "b": "5", "c": "5", "function": "complex_public_method"}))
    t.execute_command({"function": "simple_public_method", "x": 22, "y": 10})
