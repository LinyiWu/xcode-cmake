from pbxproj.PBXObject import PBXObject
from pbxproj.PBXNativeTarget import PBXNativeTarget
from pbxproj.XCConfigurationList import XCConfigurationList
from typing import Callable
import json


class PBXProject(PBXObject):
    def __init__(self, idstr, objects) -> None:
        super().__init__(idstr, objects)
        assert(self.isa == "PBXProject")
        # the minimum that I care
        self.buildConfigurationList = XCConfigurationList.new(
            self._data["buildConfigurationList"], objects)
        self.targets: list[PBXNativeTarget] = []
        for idstr in self._data["targets"]:
            self.targets.append(PBXNativeTarget.new(idstr, objects))
        return

    @classmethod
    def new_from_file(cls, file):
        cls.clear()
        with open(file, "r") as fi:
            proj = json.load(fi)
        objects = proj["objects"]
        rootObjectIDStr = proj["rootObject"]
        return PBXProject.new(rootObjectIDStr, objects)

    def parse_project_build_settings(self, invoke: Callable[[str, str, str], None]):
        self.buildConfigurationList.parse_build_settings(invoke)
        return

    def parse_targets_build_settings(self, invoke: Callable[[str, str, str], None]):
        for i in self.targets:
            i.parse_build_settings(invoke)
        return
