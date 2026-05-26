from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Signal:
    signal_id: Optional[str]
    correlation_id: Optional[str]
    event_type: str
    message: str
    payload: dict[str, object] = field(default_factory=dict)
