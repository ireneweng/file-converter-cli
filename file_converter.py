import importlib
import json
import pandas
import yaml
from json2html import *
from pathlib import Path

PLUGIN_DIR = "plugins"


class LoadPluginError(Exception):
    """Custom exception to handle plugin loading errors."""

    def __init__(self, mod_name, e, func_name=None):
        func_str = f"'{func_name}' from" if func_name else ""
        self.message = f"Error loading {func_str}{mod_name}: {e}"
        super().__init__(self.message)


class FileConverter(object):
    """File format converter, with the option to use custom user-defined
    conversion plugins.

    Supported inputs: csv, json
    Supported outputs: html, yaml
    """

    def __init__(
        self,
        input_file,
        output_file,
        plugin=None,
        plugin_dir=PLUGIN_DIR,
        read_func=None,
        write_func=None,
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.plugin = plugin
        self.plugin_dir = plugin_dir
        self.read_func = read_func
        self.write_func = write_func

    @staticmethod
    def load_module(mod_name, plugin_dir=PLUGIN_DIR):
        try:
            module = importlib.import_module(f".{mod_name}", plugin_dir)
            return module
        except Exception as e:
            raise LoadPluginError(mod_name, e)

    @staticmethod
    def load_func(module, func_name):
        try:
            func = getattr(module, func_name)
            return func
        except Exception as e:
            raise LoadPluginError(module.__name__, e, func_name=func_name)

    @staticmethod
    def load_json(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data

    def convert_file(self):
        success_msg = f"'{self.input_file}' successfully converted to '{self.output_file}'"
        input_type = self._get_file_type(self.input_file)
        output_type = self._get_file_type(self.output_file)

        # use custom plugin function if provided
        if self.plugin:
            mod_name, func_name = self._get_mod_names(self.plugin)
            module = self.load_module(mod_name, plugin_dir=self.plugin_dir)

            # use custom reader and writer if provided
            if not func_name:
                if not (self.read_func and self.write_func):
                    raise ValueError(
                        "Must provide both read and write functions."
                    )
                result = self._custom_read_write_file(
                    module, self.read_func, self.write_func
                )
                print(success_msg)
                return result

            func = self.load_func(module, func_name)

        # default to builtin conversion function
        else:
            func_name = f"{input_type}_to_{output_type}"
            func = getattr(self, func_name, None)

        if not func:
            raise TypeError(
                f"Conversion from {input_type} to {output_type} not supported"
            )
        result = func(self.input_file, self.output_file)
        print(success_msg)
        return result

    # ----------------
    # Helper Functions
    # ----------------

    def _get_file_type(self, filename):
        return (Path(filename).suffix).replace(".", "")

    def _get_mod_names(self, plugin_name):
        plugin = plugin_name.split(".")
        if len(plugin) == 1:
            return (plugin[0], "")
        elif len(plugin) == 2:
            mod_name, func_name = plugin
            return (mod_name, func_name)
        else:
            raise TypeError("Invalid plugin format provided")

    def _custom_read_write_file(self, module, read_func, write_func):
        reader = self.load_func(module, read_func)
        writer = self.load_func(module, write_func)
        data = reader(self.input_file)
        result = writer(data, self.output_file)
        return result

    # --------------------
    # Conversion Functions
    # --------------------

    def csv_to_html(self, input, output):
        data = pandas.read_csv(input)
        data.to_html(output)
        return True

    def csv_to_yaml(self, input, output):
        data = pandas.read_csv(input).to_dict(orient="records")
        with open(output, "w") as f:
            yaml.dump(data, f, sort_keys=False)
        return True

    def json_to_html(self, input, output):
        data = self.load_json(input)
        result = json2html.convert(json=data)
        with open(output, "w") as f:
            f.write(result)
        return True

    def json_to_yaml(self, input, output):
        data = self.load_json(input)
        with open(output, "w") as f:
            yaml.dump(data, f)
        return True
