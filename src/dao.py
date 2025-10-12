from datetime import datetime
from typing import Optional

from domain import Lot, LotStatus


def find_lot(bids_table, lot_id: str) -> Optional[Lot]:
    response = bids_table.get_item(
        Key={"PK": f"LOT#{lot_id}"},
        ConsistentRead=True,
    )

    item = response.get('Item')
    if item is None:
        return None

    lot = Lot(
        id=item['id'],
        name=item['name'],
        status=LotStatus[item['status']],
        highest_bid_id=item.get('highest_bid_id'),
        highest_bid_amount=item.get('highest_bid_amount'),
        time_opened=datetime.fromisoformat(item['time_opened']) if item.get('time_opened') is not None else None,
        time_closed=datetime.fromisoformat(item['time_closed']) if item.get('time_closed') is not None else None
    )

    return lot
