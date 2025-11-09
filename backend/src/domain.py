from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import Optional, TypeVar, Generic
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
            "userId": self.user_id,
            "lotId": self.lot_id,
            "amount": self.amount,
            "timePlaced": self.time_placed.isoformat(),
            "timeProcessed": self.time_processed.isoformat() \
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
    image_url: Optional[str] = None
    highest_bid_id: Optional[str] = None
    highest_bid_amount: Optional[Decimal] = None
    time_opened: Optional[datetime] = None
    time_closed: Optional[datetime] = None

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.name,
            "image_url": self.image_url,
            "highestBidId": self.highest_bid_id \
                if (self.highest_bid_id is not None) else None,
            "highestBidAmount": str(self.highest_bid_amount) \
                if (self.highest_bid_amount is not None) else None,
            "timeOpened": self.time_opened.isoformat()
            if (self.time_opened is not None) else None,
            "timeClosed": self.time_closed.isoformat() \
                if (self.time_closed is not None) else None
        }


T = TypeVar("T")


@dataclass
class PaginatedList(Generic[T]):
    data: list[T]
    limit: int
    start_key: str | None
    last_key: str | None
