import "./page.css";
import { Container, Grid } from "@mui/material";
import LotCard from "../../components/LotCard";
import React, { useEffect, useState } from "react";
import { fetchAllLots } from "../../services/LotService";
import { Lot } from "../../services/types/LotService";

const LotsPage: React.FC = () => {
  const [lots, setLots] = useState<Array<Lot>>([]);

  useEffect(() => {
    const fetchLots = async () => {
      const { data } = await fetchAllLots();
      console.log({ data });
      setLots(data);
    };

    fetchLots();
  }, []);

  return (
    <div className="App">
      <Container>
        <header className="App-header">
          <img src="pokeball.png" className="App-logo" alt="logo" />
        </header>
        <Grid
          paddingTop={4}
          container
          spacing={{ xs: 2, md: 3 }}
          columns={{ xs: 4, sm: 8, md: 12 }}
        >
          {lots.map((lot, index) => (
            <Grid size={4} key={index}>
              <LotCard
                lotName={lot.name}
                highestBid={lot.highestBidAmount}
                imagerUrl={lot.imageUrl}
              />
            </Grid>
          ))}
        </Grid>
      </Container>
    </div>
  );
};

export default LotsPage;
