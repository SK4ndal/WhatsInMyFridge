import type { CategoryGroup, Foodstuff, FoodstuffFormState, InventoryFormState, InventoryItem } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

export function listInventory(): Promise<InventoryItem[]> {
  return request<InventoryItem[]>("/inventory");
}

export function listGroupedInventory(): Promise<CategoryGroup[]> {
  return request<CategoryGroup[]>("/inventory/grouped-by-category");
}

export function listFoodstuffs(search?: string): Promise<Foodstuff[]> {
  const params = search ? `?search=${encodeURIComponent(search)}` : "";
  return request<Foodstuff[]>(`/foodstuffs${params}`);
}

export function createFoodstuff(form: FoodstuffFormState): Promise<Foodstuff> {
  return request<Foodstuff>("/foodstuffs", {
    method: "POST",
    body: JSON.stringify({
      name: form.name,
      category: form.category,
      expiry_min_days: Number(form.expiryMinDays),
      expiry_max_days: Number(form.expiryMaxDays),
    }),
  });
}

export function createInventoryItem(form: InventoryFormState): Promise<InventoryItem> {
  return request<InventoryItem>("/inventory", {
    method: "POST",
    body: JSON.stringify(toPayload(form)),
  });
}

export function updateInventoryItem(id: number, form: InventoryFormState): Promise<InventoryItem> {
  return request<InventoryItem>(`/inventory/${id}`, {
    method: "PATCH",
    body: JSON.stringify(toPayload(form)),
  });
}

export function removeInventoryItem(id: number): Promise<void> {
  return request<void>(`/inventory/${id}`, { method: "DELETE" });
}

function toPayload(form: InventoryFormState) {
  return {
    foodstuff_id: form.foodstuffId ? Number(form.foodstuffId) : null,
    name: form.name || null,
    category: form.category || null,
    quantity_amount: form.quantityAmount,
    quantity_unit: form.quantityUnit,
    purchase_date: form.purchaseDate,
    estimated_expiry_date: form.estimatedExpiryDate || null,
  };
}
