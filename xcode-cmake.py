#!/usr/bin/env python3
from pbxproj.PBXProject import PBXProject
from pbxproj.PBXNativeTarget import PBXNativeTarget
from typing import Callable
import argparse
import os


# CMAKE_CONFIGURATION_TYPES
#   [Debug, Release, MinSizeRel, RelWithDebInfo]
XCodeDefaultConfigurations = {"Debug", "Release"}


class X2CAttributes:
    def __init__(self) -> None:
        self.dd = {}
        return

    def add(self, config: str, k: str, v: str) -> None:
        assert(config in XCodeDefaultConfigurations)
        if k not in self.dd:
            self.dd[k] = {}
        self.dd[k][config] = v
        return

    def dump(self, invoke: Callable[[str, str, str], str]) -> None:
        """
        invoke(c, k, v)
        """
        for (k, cv) in self.dd.items():
            cv: dict
            if (set(cv.keys()) == XCodeDefaultConfigurations and
                    len(set(cv.values())) == 1):
                invoke('', k, list(cv.values())[0])
            else:
                for (config, v) in cv.items():
                    if config == "Debug":
                        invoke(f'[variant={config}]', k, v)
                    else:
                        for config in ["Release", "MinSizeRel", "RelWithDebInfo"]:
                            invoke(f'[variant={config}]', k, v)
        return


def mk_project_attr(c: str, k: str, v: str) -> str:
    return f'set(CMAKE_XCODE_ATTRIBUTE_{k}{c} "{v}")\n'


def mk_targets_attr(c: str, k: str, v: str) -> str:
    return f'XCODE_ATTRIBUTE_{k}{c} "{v}"\n'


def main(input: str, output: str):
    rootObject: PBXProject = PBXProject.new_from_file(input)
    with open(os.path.join(output, "xcode_attr.cmake"), "w") as fo:
        attr = X2CAttributes()
        rootObject.parse_project_build_settings(
            lambda config, k, v: attr.add(config, k, v))
        attr.dump(lambda c, k, v: fo.write(mk_project_attr(c, k, v)))

    for target in rootObject.targets:
        target: PBXNativeTarget
        with open(os.path.join(output, f"{target.name}.cmake"), "w") as fo:
            fo.write(f"set_target_properties({target.name} PROPERTIES\n")
            attr = X2CAttributes()
            target.parse_build_settings(
                lambda config, k, v: attr.add(config, k, v))
            attr.dump(lambda c, k, v: fo.write(mk_targets_attr(c, k, v)))
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
