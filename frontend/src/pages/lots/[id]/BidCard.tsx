import { Box, Card, CardContent, Typography } from "@mui/material";
import { formatCurrency, formatDateTime } from "../../../services/utils";
import { Lot } from "../../../services/types/LotService";

interface BidCardProps {
  lot: Lot;
}

const BidCard: React.FC<BidCardProps> = ({ lot }) => {
  return (
    <Card sx={{ p: 2 }} variant="outlined">
      <CardContent>
        <Typography sx={{ color: "text.secondary" }} gutterBottom>
          Highest Bid
        </Typography>
        {lot.highestBidAmount && (
          <Typography variant="h3">
            {formatCurrency(lot.highestBidAmount)}
          </Typography>
        )}
        {lot.timeOpened && (
          <Typography sx={{ color: "text.secondary" }}>
            Time Placed:{" "}
            <Box component="span" sx={{ fontWeight: 700 }}>
              {formatDateTime(new Date(lot.timeOpened))}
            </Box>
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default BidCard;
