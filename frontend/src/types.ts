export type Foodstuff = {
  id: number;
  name: string;
  category: string;
  expiry_min_days: number;
  expiry_max_days: number;
  notes?: string | null;
};

export type InventoryItem = {
  id: number;
  foodstuff_id?: number | null;
  name: string;
  category: string;
  quantity_amount: string;
  quantity_unit: string;
  purchase_date: string;
  estimated_expiry_date: string;
  is_active: boolean;
  foodstuff?: Foodstuff | null;
};

export type CategoryGroup = {
  category: string;
  items: InventoryItem[];
};

export type InventoryFormState = {
  foodstuffId: string;
  name: string;
  category: string;
  quantityAmount: string;
  quantityUnit: string;
  purchaseDate: string;
  estimatedExpiryDate: string;
};

export type FoodstuffFormState = {
  name: string;
  category: string;
  expiryMinDays: string;
  expiryMaxDays: string;
};
