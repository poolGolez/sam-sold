import { Box, Card, CardContent, CardMedia, Typography } from "@mui/material";
import React from "react";

interface LotCardProps {
  lotName: string;
  highestBid?: number;
}

const LotCard: React.FC<LotCardProps> = ({ lotName, highestBid = 0.0 }) => {
  return (
    <Card sx={{ display: "flex" }}>
      <Box sx={{ display: "flex", flexDirection: "column", width: "75%" }}>
        <CardContent sx={{ flex: "1 0 auto" }}>
          <Typography component="div" variant="h5">
            {highestBid}
          </Typography>
          <Typography
            variant="subtitle1"
            component="div"
            sx={{ color: "text.secondary" }}
          >
            {lotName}
          </Typography>
        </CardContent>
      </Box>
      <CardMedia
        component="img"
        sx={{ width: 151 }}
        image="/pokeball.png"
        alt="Pokeball"
      />
    </Card>
  );
};

export default LotCard;
