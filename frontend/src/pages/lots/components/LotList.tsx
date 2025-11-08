import { Grid } from "@mui/material";
import LotCard from "./LotCard";
import React from "react";
import { Lot } from "../../../services/types/LotService";

interface LotsListProps {
  lots: Lot[];
}

const LotList: React.FC<LotsListProps> = ({ lots }) => {
  return (
    <Grid
      paddingTop={4}
      container
      spacing={{ xs: 2, md: 3 }}
      columns={{ xs: 4, sm: 8, md: 12 }}
    >
      {lots.map((lot, index) => (
        <Grid size={4} key={index}>
          <LotCard lot={lot} />
        </Grid>
      ))}
    </Grid>
  );
};

export default LotList;
