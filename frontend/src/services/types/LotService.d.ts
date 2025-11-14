export interface Lot {
  id: string;
  name: string;
  status: string;
  imageUrl?: string;
  highestBidId?: string;
  highestBidAmount?: number;
  timeOpened: string;
}

export interface Bid {
  id: string;
  amount: number;
  userId: string;
  timePlaced: Date;
  timeProcessed?: Date;
}

interface BidApiResponse {
  id: string;
  amount: number;
  user_id: string;
  time_placed: string;
  time_processed?: string;
}
