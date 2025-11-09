import { Card, CardContent, Typography } from "@mui/material";

interface BidCardProps {
  highestBidAmount: number;
}

const BidCard: React.FC<BidCardProps> = ({ highestBidAmount }) => {
  return (
    <Card sx={{ p: 2 }} variant="outlined">
      <CardContent>
        <Typography sx={{ color: "text.secondary" }} gutterBottom>
          Highest Bid
        </Typography>
        <Typography variant="h3">{highestBidAmount}</Typography>
        <Typography sx={{ color: "text.secondary" }}>
          {`Time placed: ${"<TODO>"}`}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default BidCard;
