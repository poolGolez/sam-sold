import "./page.css";
import { Container } from "@mui/material";
import React from "react";
import { Outlet } from "react-router-dom";

const LotsLayout: React.FC = () => {
  const header = (
    <header className="App-header">
      <img src="/pokeball.png" className="App-logo" alt="logo" />
    </header>
  );

  return (
    <div className="App">
      <Container>
        {header}
        <Outlet />
      </Container>
    </div>
  );
};

export default LotsLayout;
