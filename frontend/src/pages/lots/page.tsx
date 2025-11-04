import "./page.css";
import React, { useEffect, useState } from "react";
import { fetchAllLots } from "../../services/LotService";
import { Lot } from "../../services/types/LotService";
import LotList from "./components/LotList";

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

  return <LotList lots={lots} />;
};

export default LotsPage;
