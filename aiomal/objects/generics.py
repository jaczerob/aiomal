from typing import Any, Dict


class Object:
    def __init__(self, data: Dict[str, Any]) -> None:
        pass


class Nullable(Object):
    def __new__(cls, data: Dict[str, Any]):
        if data is None:
            return None

        return super(Object, cls).__new__(cls)


    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)

