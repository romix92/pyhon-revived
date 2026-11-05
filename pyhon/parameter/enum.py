import logging

from typing import Dict, Any, List

from pyhon.parameter.base import HonParameter

_LOGGER = logging.getLogger(__name__)


def clean_value(value: str | float) -> str:
    return str(value).strip("[]").replace("|", "_").lower()


class HonParameterEnum(HonParameter):
    def __init__(self, key: str, attributes: Dict[str, Any], group: str) -> None:
        super().__init__(key, attributes, group)
        self._default: str | float = ""
        self._value: str | float = ""
        self._values: List[str] = []
        self._set_attributes()
        if self._default and clean_value(self._default.strip("[]")) not in self.values:
            self._values.append(self._default)
        if self._values and clean_value(self._value) not in self.values:
            self._value = self.values[0]

    def _set_attributes(self) -> None:
        super()._set_attributes()
        self._default = self._attributes.get("defaultValue", "")
        self._values = self._attributes.get("enumValues", [])
        if self._default:
            self._value = self._default
        elif self._values:
            self._value = clean_value(self._values[0])
        else:
            self._value = "0"

    def __repr__(self) -> str:
        return f"{self.__class__} (<{self.key}> {self.values})"

    @property
    def values(self) -> List[str]:
        return [clean_value(value) for value in self._values]

    @values.setter
    def values(self, values: List[str]) -> None:
        self._values = values
        if self._default and clean_value(self._default.strip("[]")) not in self.values:
            self._values.append(self._default)
        if self._values and clean_value(self._value) not in self.values:
            self._value = self.values[0]
        _LOGGER.info(
            "Set values of %s to %s", str(self._key), str(self._values)
        )

    @property
    def intern_value(self) -> str:
        return str(self.value)

    @property
    def value(self) -> str | float:
        if self._value is not None:
            cleaned = clean_value(self._value)
            if not self.values or cleaned in self.values:
                return cleaned
        return self.values[0] if self.values else "0"

    @value.setter
    def value(self, value: str) -> None:
        cleaned = clean_value(value)
        if cleaned in self.values:
            self._value = value
            self.check_trigger(cleaned)
        elif str(value) in self.values:
            self._value = value
            self.check_trigger(str(value))
        else:
            raise ValueError(f"Allowed values: {self._values} But was: {value}")
