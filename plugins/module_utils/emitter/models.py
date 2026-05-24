from dataclasses import dataclass, field
from typing import Any


@dataclass
class Signal:
    event_type: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
