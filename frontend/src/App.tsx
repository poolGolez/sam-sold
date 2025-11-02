import logo from "./logo.svg";
import "./App.css";
import { Container, Grid } from "@mui/material";
import LotCard from "./components/LotCard";

const lots = [
  {
    name: "Shiny Magmar",
    highestBidAmount: 25.31,
    imageUrl: "/images/pokemon/shiny-magmar.webp",
  },
  {
    name: "Galarian Ponyta",
    highestBidAmount: 22.1,
    imageUrl: "/images/pokemon/galarian-ponyta.png",
  },
  {
    name: "Pokemon Egg",
    highestBidAmount: 30.45,
    imageUrl: "/images/pokemon/pokemon-egg.jpeg",
  },
  {
    name: "Celebi",
    highestBidAmount: 27.89,
    imageUrl: "/images/pokemon/celebi.webp",
  },
  {
    name: "Dark Mimikyu",
    highestBidAmount: 35.0,
    imageUrl: "/images/pokemon/dark-mimikyu.png",
  },
  {
    name: "Shiny Gardevoir",
    highestBidAmount: 29.75,
    imageUrl: "/images/pokemon/shiny-gardevoir.png",
  },
];

function App() {
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
}

export default App;
