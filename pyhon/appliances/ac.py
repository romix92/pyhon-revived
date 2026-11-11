from contextlib import suppress
from typing import Any, Dict

from pyhon.appliances.base import ApplianceBase


class Appliance(ApplianceBase):
    def attributes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data = super().attributes(data)
        params = data.get("parameters", {})
        mach_mode = params.get("machMode")
        raw_mach = mach_mode.value if hasattr(mach_mode, "value") else mach_mode
        try:
            mach_val = str(int(float(raw_mach)))
        except (ValueError, TypeError):
            mach_val = str(raw_mach)

        health_mode = params.get("healthMode")
        raw_health = health_mode.value if hasattr(health_mode, "value") else health_mode
        try:
            health_val = str(int(float(raw_health)))
        except (ValueError, TypeError):
            health_val = str(raw_health)

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
        raw_on_off = on_off.value if hasattr(on_off, "value") else on_off
        try:
            on_off_val = str(int(float(raw_on_off)))
        except (ValueError, TypeError):
            on_off_val = str(raw_on_off)
        data["active"] = on_off_val == "1"
        return data

    def settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        return settings
