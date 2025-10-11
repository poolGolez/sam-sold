from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
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

class LotStatus(Enum):
    DRAFT = auto()
    OPEN = auto()
    CLOSED = auto()


@dataclass(frozen=True)
class Lot:
    id: str
    name: str
    status: LotStatus = LotStatus.DRAFT
    highest_bid_id: Optional[str] = None
    highest_bid_amount: Optional[Decimal] = None
    time_opened: Optional[datetime] = None
    time_closed: Optional[datetime] = None
