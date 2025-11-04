import api from "./api";
import { Lot } from "./types/LotService";

export const fetchAllLots = async (): Promise<{
  data: Array<Lot>
}> => {
  const response = await api.get("/lots");
  return response.data as {
    data: Array<Lot>
  };
};
