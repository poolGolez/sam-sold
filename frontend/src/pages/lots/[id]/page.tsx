import { useEffect, useState } from "react";
import { fetchBidsByLotId, fetchLotById } from "../../../services/LotService";
import { Bid, Lot } from "../../../services/types/LotService";
import { useParams } from "react-router-dom";
import LotCard from "./LotCard";
import { Box, Grid } from "@mui/material";
import BidCard from "./BidCard";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { formatDateTime } from "../../../services/utils";
import { useWebSocket } from "../../../services/websocket";
const LotPage: React.FC = () => {
  const [lot, setLot] = useState<Lot | null>(null);
  const [bids, setBids] = useState<Bid[]>([]);
  const { id } = useParams();

  const onLotChangeBroadcasted = ({ data }: MessageEvent) => {
    const jsonData = JSON.parse(data);
    const updatedLot = jsonData.lot as Lot;
    setLot({ ...lot, ...updatedLot });
  };

  useWebSocket(
    `wss://9ejotlcle8.execute-api.ap-southeast-1.amazonaws.com/dev?user-id=react-1&lot-id=${1024}`,
    onLotChangeBroadcasted
  );

  useEffect(() => {
    const fetchLotDetails = async () => {
      const lotData = await fetchLotById(id!);
      setLot(lotData);

      const bidsData = await fetchBidsByLotId(id!);
      setBids(bidsData);
    };

    fetchLotDetails();
  }, [id]);

  if (!lot) {
    return <div>Loading...</div>;
  }

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 250 },
    { field: "amount", headerName: "Amount", width: 100 },
    { field: "userId", headerName: "User ID", width: 250 },
    {
      field: "timePlaced",
      headerName: "Time Placed",
      width: 300,
      valueFormatter: (value) => {
        if (!value) return "";

        return formatDateTime(value);
      },
    },
  ];

  return (
    <Grid container spacing={1} sx={{ pt: 2 }}>
      <Grid size={{ xs: 12, md: 3 }}>
        <LotCard lot={lot} />
      </Grid>

      {lot && (
        <Grid size={{ xs: 12, md: 9 }}>
          <BidCard lot={lot} />

          {bids && (
            <Box sx={{ width: "100%" }}>
              <DataGrid
                rows={bids}
                columns={columns}
                disableRowSelectionOnClick
              />
            </Box>
          )}
        </Grid>
      )}
    </Grid>
  );
};

export default LotPage;
