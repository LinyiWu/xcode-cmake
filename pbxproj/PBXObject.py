'''
PBXObject => an entry in "objects"
'''


class PBXObject:
    def __init__(self, idstr, objects) -> None:
        self._idstr: str = idstr
        self._data: dict = objects[idstr]
        self.isa: str = self._data["isa"]
        return

    _record = dict()

    @classmethod
    def new(cls, idstr: str, objects: dict):
        if idstr in cls._record:
            return cls._record[idstr]
        instance = cls(idstr, objects)
        cls._record[idstr] = instance
        return instance

    @classmethod
    def clear(cls) -> None:
        cls._record.clear()
        return
