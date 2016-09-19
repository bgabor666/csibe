#!/usr/bin/env python

import argparse
from string import Template

def generate_toolchain(template_path, toolchain_path, cc_path, cxx_path):
    with open(template_path, 'r') as input_file:
        with open(toolchain_path, 'w') as output_file:
            input_file_as_string = input_file.read()
            input_file_as_template = Template(input_file_as_string)

            output_file_as_string = input_file_as_template.safe_substitute(
                                        c_compiler_path=cc_path,
                                        cpp_compiler_path=cxx_path)
            output_file.write(output_file_as_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--template-path")
    parser.add_argument("--toolchain-path")
    parser.add_argument("--cc-path")
    parser.add_argument("--cxx-path")

    args = parser.parse_args()

    generate_toolchain(args.template_path,
                       args.toolchain_path,
                       args.cc_path,
                       args.cxx_path)
