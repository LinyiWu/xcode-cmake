from pbxproj.PBXObject import PBXObject
from typing import Callable


class XCBuildConfiguration(PBXObject):
    def __init__(self, idstr, objects) -> None:
        super().__init__(idstr, objects)
        assert(self.isa == "XCBuildConfiguration")
        self.buildSettings: dict = self._data["buildSettings"]
        self.name = self._data["name"]
        return

    def parse_build_settings(self, invoke: Callable[[str, str, str], None]):
        for (k, v) in self.buildSettings.items():
            if isinstance(v, list):
                v = set(v) - {"$(inherited)"}
                v = " ".join(v)
            assert(isinstance(v, str))
            invoke(self.name, k, v)
        return
