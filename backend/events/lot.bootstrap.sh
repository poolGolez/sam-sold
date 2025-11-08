aws dynamodb batch-write-item --request-items '{
  "SamSold-Bids": [
    {
      "PutRequest": {
        "Item": {
          "PK": {"S": "LOT#1024"},
          "LotGsiKey": {"S": "LOT#1024"},
          "id": {"S": "1024"},
          "name": {"S": "Shiny Magmar"},
          "status": {"S":"OPEN"},
          "time_opened": {"S":"2025-02-18T06:37:59.03365"},
          "image_url": {"S": "/images/pokemon/shiny-magmar.webp"}
        }
      }
    },
    {
      "PutRequest": {
        "Item": {
          "PK": {"S": "LOT#1025"},
          "LotGsiKey": {"S": "LOT#1025"},
          "id": {"S": "1025"},
          "name": {"S": "Galarian Ponyta"},
          "status": {"S":"OPEN"},
          "time_opened": {"S":"2025-02-18T06:37:59.03365"},
          "image_url": {"S": "/images/pokemon/galarian-ponyta.png"}
        }
      }
    },
    {
      "PutRequest": {
        "Item": {
          "PK": {"S": "LOT#1026"},
          "LotGsiKey": {"S": "LOT#1026"},
          "id": {"S": "1026"},
          "name": {"S": "Pokemon Egg"},
          "status": {"S":"OPEN"},
          "time_opened": {"S":"2025-02-18T06:37:59.03365"},
          "image_url": {"S": "/images/pokemon/pokemon-egg.jpeg"}
        }
      }
    },
    {
      "PutRequest": {
        "Item": {
          "PK": {"S": "LOT#1027"},
          "LotGsiKey": {"S": "LOT#1027"},
          "id": {"S": "1027"},
          "name": {"S": "Celebi"},
          "status": {"S":"OPEN"},
          "time_opened": {"S":"2025-02-18T06:37:59.03365"},
          "image_url": {"S": "/images/pokemon/celebi.webp"}
        }
      }
    },
    {
      "PutRequest": {
        "Item": {
          "PK": {"S": "LOT#1028"},
          "LotGsiKey": {"S": "LOT#1028"},
          "id": {"S": "1028"},
          "name": {"S": "Dark Mimikyu"},
          "status": {"S":"OPEN"},
          "time_opened": {"S":"2025-02-18T06:37:59.03365"},
          "image_url": {"S": "/images/pokemon/dark-mimikyu.png"}
        }
      }
    },
    {
      "PutRequest": {
        "Item": {
          "PK": {"S": "LOT#1029"},
          "LotGsiKey": {"S": "LOT#1029"},
          "id": {"S": "1029"},
          "name": {"S": "Shiny Gardevoir"},
          "status": {"S":"OPEN"},
          "time_opened": {"S":"2025-02-18T06:37:59.03365"},
          "image_url": {"S": "/images/pokemon/shiny-gardevoir.png"}
        }
      }
    }
  ]
}';

aws dynamodb scan \
  --table-name SamSold-Bids \
  --key-condition-expression "begins_with(PK, :prefix)" \
  --expression-attribute-values '{":prefix":{"S":"LOT#"}}'
