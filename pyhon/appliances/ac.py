from contextlib import suppress
from typing import Any, Dict

from pyhon.appliances.base import ApplianceBase


class Appliance(ApplianceBase):
    def attributes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data = super().attributes(data)
        params = data.get("parameters", {})
        mach_mode = params.get("machMode")
        mach_val = str(mach_mode.value if hasattr(mach_mode, "value") else mach_mode)

        health_mode = params.get("healthMode")
        health_val = str(health_mode.value if hasattr(health_mode, "value") else health_mode)

        # Map machMode to hOn program names for AC
        if health_val == "1":
            ac_mode_map = {
                "0": "iot_uv_and_auto",
                "1": "iot_uv_and_cool",
                "2": "iot_uv_and_cool",
                "3": "iot_uv_and_dry",
                "4": "iot_uv_and_heat",
                "5": "iot_uv_and_fan",
                "6": "iot_uv_and_fan",
            }
        else:
            ac_mode_map = {
                "0": "iot_auto",
                "1": "iot_cool",
                "2": "iot_cool",
                "3": "iot_dry",
                "4": "iot_heat",
                "5": "iot_fan",
                "6": "iot_fan",
            }
        if mach_val in ac_mode_map:
            program_name = ac_mode_map[mach_val]
            data["programName"] = program_name
            if start_cmd := self.parent.settings.get("startProgram.program"):
                with suppress(ValueError):
                    start_cmd.value = program_name

        on_off = params.get("onOffStatus")
        on_off_val = str(on_off.value if hasattr(on_off, "value") else on_off)
        data["active"] = on_off_val == "1"
        return data

    def settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        return settings

