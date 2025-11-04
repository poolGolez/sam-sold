export interface Lot {
  id: string;
  name: string;
  status: string;
  imageUrl?: string;
  highestBidId?: string;
  highestBidAmount?: number;
  timeOpened: string;
}