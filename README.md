# File Converter CLI
A simple file conversion tool with support for user-defined conversion plugins.

## Overview
This is a very basic demo of a Python command-line interface, originally completed in one week for a coding test.

### Requirements
- Python 3
- [json2html](https://pypi.org/project/json2html/)
- [pandas](https://pandas.pydata.org/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [toml](https://pypi.org/project/toml/)

### Package Files
- [`convert`](convert): executable script containing the CLI tool used to parse user input
- [`file_converter.py`](file_converter.py): module used to process and run the file conversions
- [`tests.py`](tests.py): module containing basic unit tests for valid user inputs
- [`/examples`](examples): folder containing example input and output files to run the program with
- [`/plugins`](plugins): default folder used by the program to search for custom implementations
    - [`my_converter.py`](my_converter.py): example module that can be passed into the CLI

### Considerations

This program currently requires one of the following for custom plugins:
- `--plugin {module name}.{function name}`
    - this runs the specified conversion function with no separation of read/write functions
    - expects the function to handle the entire conversion process
- `--plugin {module name} --reader {read function name} --writer {write function name}`
    - this finds the read and write functions inside the specified module and runs them together to convert a file
    - expects the output of the read function to be a valid input to the write function

A different implementation could dynamically find and run functions inside a module which adhere to a specific naming convention. This would make the CLI input much simpler by only requiring `--plugin {module name}` and removing the need for `--reader` and `--writer` flags. Also, the tool would not need to parse and process so many different combinations of inputs. The trade-off would be more checks to validate the module's contents conform to more rules.

There are no checks to ensure custom read/write functions match the output file type, so this works:

    ./convert examples/colors.json examples/colors.toml --plugin my_converter -r read_json -w write_yaml

It is up to the user to provide the correct arguments.

### Areas of Improvement
- Process conditional arguments using a subparser instead of printing errors/warnings and re-setting arg variables
- Use better way of getting file type from input and output files
    - for example, the current method excludes `.yml` files from yaml conversion
- More customization via command-line options
- More robust error and exception handling
- Better test coverage and more detailed tests, currently only checks return code success/failure
- Use cleaner and more robust separation between read and write functions
- Create custom data structure for storing data between read/write functionality
    - conversions between file formats would be much easier, but this requires much more custom/manual processing
- Find better ways of parsing and using package/module/function names, i.e. utilizing `importlib.import_module` args better

## Usage

At its most basic, users need to provide an input file and destination output file path:

    ./convert {input file} {output file}
    ./convert examples/colors.json examples/colors.yaml

### Built-in Support
To add built-in support for more file formats, a user can add conversion functions to `file_converter.py`.\
Function names must follow this naming convention: `{input file type}_to_{output file type}`\
For example: `json_to_yaml`

### User-Defined Plugins
Without modifying the main program, a user can add their conversion module to `/plugins` or their own package.

To run the program with a custom function:

    ./convert {input file} {output file} --plugin {module name}.{function name}
    ./convert examples/colors.json examples/colors.yaml --plugin my_converter.json_to_yaml

To run with a custom function inside a different package:

    ./convert {input file} {output file} --plugin {module name}.{function name} --package {package name}
    ./convert examples/colors.json examples/colors.yaml --plugin my_converter.json_to_yaml --package my_plugins

To run a module's custom read and write functions:

    ./convert {input file} {output file} --plugin {module name} --reader {read function} --writer {write function}
    ./convert examples/colors.json examples/colors.yaml --plugin my_converter -r read_json -w write_yaml
