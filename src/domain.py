from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4


@dataclass(frozen=True)
class Bid:
    user_id: str
    lot_id: str
    amount: Decimal
    time_placed: datetime
    time_processed: Optional[datetime] = None
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "lot_id": self.lot_id,
            "amount": self.amount,
            "time_placed": self.time_placed.isoformat(),
            "time_processed": self.time_processed.isoformat() \
                if (self.time_processed is not None) else None
        }
