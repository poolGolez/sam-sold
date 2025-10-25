aws dynamodb put-item \
  --table-name 'SamSold-Bids' \
  --item '{
   "PK": {"S": "LOT#1024"},
   "id": {"S": "1024"},
   "name": {"S": "Shiny Magmar"},
   "status": {"S":"OPEN"},
   "time_opened": {"S":"2025-02-18T06:37:59.03365"}
  }'

aws dynamodb put-item \
  --table-name 'SamSold-Bids' \
  --item '{
   "PK": {"S": "LOT#512"},
   "id": {"S": "512"},
   "name": {"S": "Ghostly Magikarp"},
   "status": {"S":"OPEN"},
   "time_opened": {"S":"2023-12-21T10:37:55.826744"}
  }'

aws dynamodb put-item \
  --table-name 'SamSold-Bids' \
  --item '{
   "PK": {"S": "LOT#32"},
   "id": {"S": "32"},
   "name": {"S": "Dark Gardevoir"},
   "status": {"S":"DRAFT"}
  }'