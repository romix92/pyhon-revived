from typing import List, TYPE_CHECKING, Dict

from pyhon.parameter.enum import HonParameterEnum

if TYPE_CHECKING:
    from pyhon.commands import HonCommand


class HonParameterProgram(HonParameterEnum):
    _FILTER = ["iot_recipe", "iot_guided"]

    def __init__(self, key: str, command: "HonCommand", group: str) -> None:
        self._command = command
        self._programs: Dict[str, "HonCommand"] = command.categories
        super().__init__(key, {}, group)
        if "PROGRAM" in command.category:
            self._value = command.category.split(".")[-1].lower()
        else:
            self._value = command.category
        self._typology: str = "enum"

    @property
    def value(self) -> str | float:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        if value in self.values:
            if self._value != value:
                self._value = value
                self._command.category = value
                self._command.appliance.sync_command("settings", self._command.name)
        else:
            raise ValueError(f"Allowed values: {self.values} But was: {value}")

    @property
    def values(self) -> List[str]:
        if not hasattr(self, "_programs") or not self._programs:
            return []
        values = [v for v in self._programs if all(f not in v for f in self._FILTER)]
        return sorted(values)

    @values.setter
    def values(self, values: List[str]) -> None:
        raise ValueError("Cant set values {values}")

    @property
    def ids(self) -> Dict[int, str]:
        values: Dict[int, str] = {}
        for name, parameter in self._programs.items():
            if "iot_" in name:
                continue
            if not parameter.parameters.get("prCode"):
                continue
            if (fav := parameter.parameters.get("favourite")) and fav.value == "1":
                continue
            values[int(parameter.parameters["prCode"].value)] = name
        return dict(sorted(values.items()))

    def set_value(self, value: str) -> None:
        self._value = value
