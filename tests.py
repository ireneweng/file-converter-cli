import subprocess
import unittest


class FileConversionTester(unittest.TestCase):
    def __init__(self):
        super(FileConversionTester, self).__init__()
        self.plugin_args = [
            "./convert",
            "examples/colors.json",
            "examples/colors.toml",
            "-p",
        ]

    def test_builtin_conversion(self):
        args = ["./convert", "examples/colors.json", "examples/colors.yaml"]
        result = subprocess.run(args, capture_output=True)
        self.assertEqual(0, result.returncode)

        args = ["./convert", "examples/colors.json", "examples/colors.toml"]
        result = subprocess.run(args, capture_output=True)
        self.assertEqual(1, result.returncode)

    def test_plugin_conversion(self):
        args = self.plugin_args + ["my_converter.json_to_toml"]
        result = subprocess.run(args, capture_output=True)
        self.assertEqual(0, result.returncode)

        args = self.plugin_args + ["my_converter."]
        result = subprocess.run(args, capture_output=True)
        self.assertNotEqual(0, result.returncode)

        args = self.plugin_args + ["my_converter.nonexistent_function"]
        result = subprocess.run(args, capture_output=True)
        self.assertNotEqual(0, result.returncode)

        args = self.plugin_args + ["my_converter.too.many.modules"]
        result = subprocess.run(args, capture_output=True)
        self.assertNotEqual(0, result.returncode)

    def test_custom_read_write(self):
        args = self.plugin_args + [
            "my_converter",
            "-r",
            "read_json",
            "-w",
            "write_toml",
        ]
        result = subprocess.run(args, capture_output=True)
        self.assertEqual(0, result.returncode)

        args = self.plugin_args + ["my_converter", "-r", "read_json"]
        result = subprocess.run(args, capture_output=True)
        self.assertNotEqual(0, result.returncode)

        args = self.plugin_args + ["my_converter" "-w", "write_toml"]
        result = subprocess.run(args, capture_output=True)
        self.assertNotEqual(0, result.returncode)

    def main(self):
        self.test_builtin_conversion()
        self.test_plugin_conversion()
        self.test_custom_read_write()


if __name__ == "__main__":
    tester = FileConversionTester()
    tester.main()
