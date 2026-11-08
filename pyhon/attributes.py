from datetime import datetime, timedelta, timezone
from typing import Optional, Final, Dict, Any

from pyhon.helper import str_to_float


def parse_timestamp(ts: Any) -> Optional[datetime]:
    if not ts or not isinstance(ts, str):
        return None
    try:
        cleaned = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


class HonAttribute:
    _LOCK_TIMEOUT: Final = 60

    def __init__(self, data: Dict[str, str] | str):
        self._value: str = ""
        self._last_update: Optional[datetime] = None
        self._lock_timestamp: Optional[datetime] = None
        self.update(data)

    @property
    def value(self) -> float | str:
        """Attribute value"""
        try:
            return str_to_float(self._value)
        except ValueError:
            return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    @property
    def last_update(self) -> Optional[datetime]:
        """Timestamp of last api update"""
        return self._last_update

    @property
    def lock(self) -> bool:
        """Shows if value changes are forbidden"""
        if not self._lock_timestamp:
            return False
        lock_until = self._lock_timestamp + timedelta(seconds=self._LOCK_TIMEOUT)
        return lock_until >= datetime.now(timezone.utc)

    def update(self, data: Dict[str, str] | str, shield: bool = False) -> bool:
        if self.lock and not shield:
            return False

        if shield:
            self._lock_timestamp = datetime.now(timezone.utc)
            self._last_update = self._lock_timestamp

        if isinstance(data, str):
            self.value = data
            return True

        incoming_ts = parse_timestamp(data.get("lastUpdate"))
        if incoming_ts and self._last_update and not shield:
            if incoming_ts < self._last_update:
                return False

        self.value = data.get("parNewVal", "")
        if incoming_ts:
            self._last_update = incoming_ts
        return True

    def __str__(self) -> str:
        return self._value
