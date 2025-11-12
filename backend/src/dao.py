import base64
import json
from datetime import datetime
from typing import Optional

from boto3.dynamodb.conditions import Key

from domain import Lot, LotStatus, PaginatedList


def find_all_lots(bids_table) -> list[Lot]:
    response = bids_table.scan(
        IndexName="LotGsi",
        Limit=20
    )

    items = response.get("Items", [])
    return [map_db_item_to_lot(item) for item in items]


def find_lot(bids_table, lot_id: str) -> Optional[Lot]:
    response = bids_table.get_item(
        Key={"PK": f"LOT#{lot_id}"},
        ConsistentRead=True,
    )

    item = response.get('Item')
    if item is None:
        return None

    lot = map_db_item_to_lot(item)

    return lot


def find_bids_by_lot(bids_table, lot: Lot, limit: int = 20, start_key=None) -> PaginatedList[Lot]:
    query = {
        "IndexName": "BidsByLotGsi",
        "KeyConditionExpression": Key("BidsByLotGsiPK").eq(f"LOT#{lot.id}"),
        "ScanIndexForward": False,
        "Limit": limit
    }

    if start_key is not None:
        query["ExclusiveStartKey"] = _decode_key(start_key)

    response = bids_table.query(**query)
    items = response.get("Items", [])
    last_key = response.get("LastEvaluatedKey")
    encoded_last_key = _encode_key(last_key) if last_key is not None else None

    return PaginatedList(
        data=items,
        limit=limit,
        start_key=start_key,
        item_count=len(items),
        last_key=encoded_last_key
    )


def map_db_item_to_lot(item):
    return Lot(
        id=item['id'],
        name=item['name'],
        status=LotStatus[item['status']],
        image_url=item.get('image_url'),
        highest_bid_id=item.get('highest_bid_id'),
        highest_bid_amount=item.get('highest_bid_amount'),
        time_opened=datetime.fromisoformat(item['time_opened']) if item.get('time_opened') is not None else None,
        time_closed=datetime.fromisoformat(item['time_closed']) if item.get('time_closed') is not None else None
    )


def _encode_key(key_obj):
    return base64.urlsafe_b64encode(json.dumps(key_obj).encode()).decode()


def _decode_key(token):
    return json.loads(base64.urlsafe_b64decode(token.encode()))
