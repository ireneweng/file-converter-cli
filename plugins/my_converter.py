import json
import toml
import yaml


# JSON Functions
def read_json(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)
    return data


def write_json(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f)
    return True


# TOML Functions
def read_toml(input_file):
    with open(input_file, "r") as f:
        data = toml.load(f)
    return data


def write_toml(data, output_file):
    with open(output_file, "w") as f:
        toml.dump(data, f)
    return True


# YAML Functions
def read_yaml(input_file):
    with open(input_file, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


def write_yaml(data, output_file):
    with open(output_file, "w") as f:
        yaml.dump(data, f)
    return True


# Conversion Functions
def json_to_toml(input_file, output_file):
    data = read_json(input_file)
    result = write_toml(data, output_file)
    return result


def json_to_yaml(input_file, output_file):
    data = read_json(input_file)
    result = write_yaml(data, output_file)
    return result


def toml_to_yaml(input_file, output_file):
    data = read_toml(input_file)
    result = write_yaml(data, output_file)
    return result


def toml_to_json(input_file, output_file):
    data = read_toml(input_file)
    result = write_json(data, output_file)
    return result


def yaml_to_toml(input_file, output_file):
    data = read_yaml(input_file)
    result = write_toml(data, output_file)
    return result


def yaml_to_json(input_file, output_file):
    data = read_yaml(input_file)
    result = write_json(data, output_file)
    return result
