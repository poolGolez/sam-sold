import { Box, Card, CardContent, CardMedia, Typography } from "@mui/material";
import React from "react";

interface LotCardProps {
  lotName: string;
  highestBid?: number;
  imagerUrl: string;
}

const LotCard: React.FC<LotCardProps> = ({
  lotName,
  highestBid = 0.0,
  imagerUrl,
}) => {
  return (
    <Card sx={{ display: "flex" }}>
      <Box sx={{ display: "flex", flexDirection: "column", width: "75%" }}>
        <CardContent sx={{ flex: "1 0 auto" }}>
          <Typography component="div" variant="h3">
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
      <Box
        sx={{
          p: 2,
          border: "1px solid lightgray",
        }}
      >
        <CardMedia
          component="img"
          sx={{ objectFit: "contain", height: "160px" }}
          image={imagerUrl}
          alt={lotName}
        />
      </Box>
    </Card>
  );
};

export default LotCard;
