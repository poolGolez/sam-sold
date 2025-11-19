import { Box, Card, CardContent, CardMedia, Typography } from "@mui/material";
import React from "react";
import { useNavigate } from "react-router-dom";
import { Lot } from "../../../services/types/LotService";
import { formatCurrency } from "../../../services/utils";

interface LotCardProps {
  lot: Lot;
}

const LotCard: React.FC<LotCardProps> = ({ lot }) => {
  const navigate = useNavigate();

  return (
    <Card
      sx={{ display: "flex", cursor: "pointer" }}
      onClick={() => navigate(`/lots/${lot.id}`)}
    >
      <Box sx={{ display: "flex", flexDirection: "column", width: "75%" }}>
        <CardContent sx={{ flex: "1 0 auto" }}>
          <Typography component="div" variant="h3">
            {lot.highestBidAmount
              ? formatCurrency(lot.highestBidAmount)
              : "No bids yet"}
          </Typography>
          <Typography
            variant="subtitle1"
            component="div"
            sx={{ color: "text.secondary" }}
          >
            {lot.name}
          </Typography>
        </CardContent>
      </Box>
      <Box sx={{ p: 2 }}>
        <CardMedia
          component="img"
          sx={{ objectFit: "contain", height: "160px" }}
          image={lot.imageUrl}
          alt={lot.name}
        />
      </Box>
    </Card>
  );
};

export default LotCard;
