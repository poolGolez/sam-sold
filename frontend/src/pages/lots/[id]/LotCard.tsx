import { Card, CardContent, CardHeader, CardMedia, Grid } from "@mui/material";
import { Lot } from "../../../services/types/LotService";

interface LotCardProps {
  lot: Lot;
}

const LotCard: React.FC<LotCardProps> = ({ lot }) => {
  return (
    <Card sx={{ p: 2 }} variant="outlined">
      <CardHeader title={lot.name} />
      <CardMedia
        component="img"
        sx={{ objectFit: "contain", height: "240px" }}
        image={lot.imageUrl}
        alt={lot.name}
      />
      <CardContent>
        <Grid container spacing={2}>
          <Grid size={6} sx={{ textAlign: "right" }}>
            Status
          </Grid>
          <Grid size={6} sx={{ textAlign: "left" }}>
            {lot.status}
          </Grid>
          <Grid size={6} sx={{ textAlign: "right" }}>
            Highest Bid
          </Grid>
          <Grid size={6} sx={{ textAlign: "left" }}>
            {lot.highestBidAmount ? `$${lot.highestBidAmount}` : "No bids yet"}
          </Grid>
          <Grid size={6} sx={{ textAlign: "right" }}>
            Time Opened
          </Grid>
          <Grid size={6} sx={{ textAlign: "left" }}>
            {lot.timeOpened
              ? new Date(lot.timeOpened).toLocaleString()
              : "Unknown"}
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default LotCard;
