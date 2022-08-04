#!/usr/bin/env python3
from pbxproj.PBXProject import PBXProject
from pbxproj.PBXNativeTarget import PBXNativeTarget
import argparse
import os


def mk_project_attr(config: str, k: str, v: str) -> str:
    # CMAKE_CONFIGURATION_TYPES
    #   [Debug, Release, MinSizeRel, RelWithDebInfo]
    # xcode default project has 2 configurations
    #   [Debug, Release]
    def attr(k, vari, v):
        return f'set(CMAKE_XCODE_ATTRIBUTE_{k}[variant={vari}] "{v}")\n'

    if config == "Debug":
        return attr(k, config, v)

    result = ""
    variants = ["Release", "MinSizeRel", "RelWithDebInfo"]
    for config in variants:
        result += attr(k, config, v)
    return result


def mk_targets_attr(config: str, k: str, v: str) -> str:
    def attr(k, vari, v):
        return f'XCODE_ATTRIBUTE_{k}[variant={vari}] "{v}"\n'

    if config == "Debug":
        return attr(k, config, v)

    result = ""
    variants = ["Release", "MinSizeRel", "RelWithDebInfo"]
    for config in variants:
        result += attr(k, config, v)
    return result


def main(input: str, output: str):
    rootObject = PBXProject.new_from_file(input)
    with open(os.path.join(output, "xcode_attr.cmake"), "w") as fo:
        rootObject.parse_project_build_settings(
            lambda a, b, c: fo.write(mk_project_attr(a, b, c)))

    for target in rootObject.targets:
        target: PBXNativeTarget
        with open(os.path.join(output, f"{target.name}.cmake"), "w") as fo:
            fo.write(f"set_target_properties({target.name} PROPERTIES\n")
            target.parse_build_settings(
                lambda a, b, c: fo.write(mk_targets_attr(a, b, c)))
            fo.write(")\n")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        Extract build configurations from xcode pbxproj for cmake.
        You should first convert project.pbxproj to json format with
        `plutil -convert json -o project.json /path/to/project.pbxproj`
        """)
    parser.add_argument("-i", "--input", help="input json file", required=True)
    parser.add_argument("-o", "--output", help="output path", required=True)
    args = parser.parse_args()
    main(args.input, args.output)
