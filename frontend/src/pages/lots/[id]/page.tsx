import { useEffect, useState } from "react";
import { fetchLotById } from "../../../services/LotService";
import { Lot } from "../../../services/types/LotService";
import { useParams } from "react-router-dom";
import LotCard from "./LotCard";
import { Grid } from "@mui/material";

const LotPage: React.FC = () => {
  const [lot, setLot] = useState<Lot | null>(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchLotDetails = async () => {
      const lotData = await fetchLotById(id!);
      setLot(lotData);
    };

    fetchLotDetails();
  }, [id]);

  if (!lot) {
    return <div>Loading...</div>;
  }

  return (
    <Grid container sx={{ pt: 2 }}>
      <Grid size={{ xs: 12, md: 4 }}>
        <LotCard lot={lot} />
      </Grid>
      <Grid size={{ xs: 12, md: 8 }}>{JSON.stringify(lot)}</Grid>
    </Grid>
  );
};

export default LotPage;
