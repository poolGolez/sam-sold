import api from "./api";
import { Bid, BidApiResponse, Lot } from "./types/LotService";

export const fetchAllLots = async (): Promise<{
  data: Array<Lot>
}> => {
  const response = await api.get("/lots");
  return response.data as {
    data: Array<Lot>
  };
};

export const fetchLotById = async (id: string): Promise<Lot> => {
  const response = await api.get(`/lots/${id}`);
  return response.data as Lot;
}

export const fetchBidsByLotId = async (lotId: string): Promise<Bid[]> => {
  const { data: { data } } = await api.get<{ data: BidApiResponse[] }>(`/lots/${lotId}/bids`);

  return data.map(({
    id,
    amount,
    user_id,
    time_placed,
    time_processed
  }: BidApiResponse): Bid => ({
    id,
    amount,
    userId: user_id,
    timePlaced: new Date(time_placed),
    timeProcessed: time_processed ? new Date(time_processed) : undefined
  }));
}
