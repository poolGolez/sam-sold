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

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.name,
            "highest_bid_id": self.highest_bid_id \
                if (self.highest_bid_id is not None) else None,
            "highest_bid_amount": str(self.highest_bid_amount) \
                if (self.highest_bid_amount is not None) else None,
            "time_opened": self.time_opened.isoformat()
                if (self.time_opened is not None) else None,
            "time_closed": self.time_closed.isoformat() \
                if (self.time_closed is not None) else None
        }
