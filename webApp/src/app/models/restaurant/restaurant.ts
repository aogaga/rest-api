export interface Restaurant {
  id: string;
  name: string;
  address?: string;
  city?: string;
  rating?: number;
  phone?: string;
  url?: string;
  categories?: string[];
  distance_meters?: number;
}
