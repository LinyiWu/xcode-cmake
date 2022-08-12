from pbxproj.PBXObject import PBXObject
from pbxproj.XCConfigurationList import XCConfigurationList
from typing import Callable


class PBXNativeTarget(PBXObject):
    def __init__(self, idstr, objects) -> None:
        super().__init__(idstr, objects)
        assert(self.isa == "PBXNativeTarget")
        self.name: str = self._data["name"]
        self.buildConfigurationList = XCConfigurationList.new(
            self._data["buildConfigurationList"], objects)
        return

    def parse_build_settings(self, invoke: Callable[[str, str, str], None]):
        """
        invoke(config, k, v)
        """
        self.buildConfigurationList.parse_build_settings(invoke)
        return
