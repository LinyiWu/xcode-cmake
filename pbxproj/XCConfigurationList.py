from pbxproj.PBXObject import PBXObject
from pbxproj.XCBuildConfiguration import XCBuildConfiguration
from typing import Callable


class XCConfigurationList(PBXObject):
    def __init__(self, idstr, objects) -> None:
        super().__init__(idstr, objects)
        assert(self.isa == "XCConfigurationList")
        self.buildConfigurations: list[XCBuildConfiguration] = []
        for idstr in self._data["buildConfigurations"]:
            self.buildConfigurations.append(
                XCBuildConfiguration.new(idstr, objects))
        return

    def parse_build_settings(self, invoke: Callable[[str, str, str], None]):
        for i in self.buildConfigurations:
            i.parse_build_settings(invoke)
        return
