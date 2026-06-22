import { FormEvent, useEffect, useMemo, useState } from "react";

import {
  createFoodstuff,
  createInventoryItem,
  listFoodstuffs,
  listGroupedInventory,
  listInventory,
  removeInventoryItem,
  updateInventoryItem,
} from "./api";
import type { CategoryGroup, Foodstuff, FoodstuffFormState, InventoryFormState, InventoryItem } from "./types";

const emptyInventoryForm: InventoryFormState = {
  foodstuffId: "",
  name: "",
  category: "",
  quantityAmount: "1.00",
  quantityUnit: "piece",
  purchaseDate: new Date().toISOString().slice(0, 10),
  estimatedExpiryDate: "",
};

const emptyFoodstuffForm: FoodstuffFormState = {
  name: "",
  category: "",
  expiryMinDays: "1",
  expiryMaxDays: "7",
};

export default function App() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [groups, setGroups] = useState<CategoryGroup[]>([]);
  const [foodstuffs, setFoodstuffs] = useState<Foodstuff[]>([]);
  const [inventoryForm, setInventoryForm] = useState<InventoryFormState>(emptyInventoryForm);
  const [foodstuffForm, setFoodstuffForm] = useState<FoodstuffFormState>(emptyFoodstuffForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [viewMode, setViewMode] = useState<"expiry" | "category">("expiry");
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    void refresh();
  }, []);

  const selectedFoodstuff = useMemo(
    () => foodstuffs.find((foodstuff) => String(foodstuff.id) === inventoryForm.foodstuffId),
    [foodstuffs, inventoryForm.foodstuffId],
  );

  async function refresh() {
    const [inventoryItems, categoryGroups, foodstuffSuggestions] = await Promise.all([
      listInventory(),
      listGroupedInventory(),
      listFoodstuffs(),
    ]);
    setItems(inventoryItems);
    setGroups(categoryGroups);
    setFoodstuffs(foodstuffSuggestions);
  }

  function applySelectedFoodstuff(foodstuffId: string) {
    const foodstuff = foodstuffs.find((candidate) => String(candidate.id) === foodstuffId);
    setInventoryForm((current) => ({
      ...current,
      foodstuffId,
      name: foodstuff?.name ?? current.name,
      category: foodstuff?.category ?? current.category,
      estimatedExpiryDate: foodstuff ? addDays(current.purchaseDate, foodstuff.expiry_max_days) : current.estimatedExpiryDate,
    }));
  }

  async function submitInventory(event: FormEvent) {
    event.preventDefault();
    if (editingId === null) {
      await createInventoryItem(inventoryForm);
      setMessage("Inventory item added. Estimated expiry remains editable.");
    } else {
      await updateInventoryItem(editingId, inventoryForm);
      setMessage("Inventory item updated.");
    }
    setInventoryForm(emptyInventoryForm);
    setEditingId(null);
    await refresh();
  }

  async function submitFoodstuff(event: FormEvent) {
    event.preventDefault();
    const foodstuff = await createFoodstuff(foodstuffForm);
    setMessage("Foodstuff created and available as a suggestion.");
    setFoodstuffForm(emptyFoodstuffForm);
    await refresh();
    applySelectedFoodstuff(String(foodstuff.id));
  }

  function editItem(item: InventoryItem) {
    setEditingId(item.id);
    setInventoryForm({
      foodstuffId: item.foodstuff_id ? String(item.foodstuff_id) : "",
      name: item.name,
      category: item.category,
      quantityAmount: item.quantity_amount,
      quantityUnit: item.quantity_unit,
      purchaseDate: item.purchase_date,
      estimatedExpiryDate: item.estimated_expiry_date,
    });
  }

  async function removeItem(item: InventoryItem) {
    await removeInventoryItem(item.id);
    setMessage("Removed from active inventory. This was not recorded as eaten or wasted.");
    await refresh();
  }

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">Core inventory foundation</p>
        <h1>What’s in my fridge?</h1>
        <p>
          Track owned food items, reusable foodstuff defaults, and estimated expiry dates without presenting them as
          food-safety guarantees.
        </p>
      </section>

      {message ? <p className="notice">{message}</p> : null}

      <section className="panel grid two-columns">
        <form onSubmit={submitInventory} className="stack">
          <h2>{editingId === null ? "Add inventory item" : "Edit inventory item"}</h2>
          <label>
            Foodstuff suggestion
            <select value={inventoryForm.foodstuffId} onChange={(event) => applySelectedFoodstuff(event.target.value)}>
              <option value="">Manual item</option>
              {foodstuffs.map((foodstuff) => (
                <option key={foodstuff.id} value={foodstuff.id}>
                  {foodstuff.name} · {foodstuff.category} · {foodstuff.expiry_min_days}-{foodstuff.expiry_max_days} days
                </option>
              ))}
            </select>
          </label>
          {selectedFoodstuff ? (
            <p className="hint">
              Defaults applied from {selectedFoodstuff.name}; name, category, quantity, and estimated expiry are still editable.
            </p>
          ) : null}
          <label>
            Name
            <input value={inventoryForm.name} onChange={(event) => setInventoryForm({ ...inventoryForm, name: event.target.value })} required />
          </label>
          <label>
            Category
            <input
              value={inventoryForm.category}
              onChange={(event) => setInventoryForm({ ...inventoryForm, category: event.target.value })}
              required
            />
          </label>
          <div className="grid compact">
            <label>
              Quantity
              <input
                type="number"
                min="0.01"
                step="0.01"
                value={inventoryForm.quantityAmount}
                onChange={(event) => setInventoryForm({ ...inventoryForm, quantityAmount: event.target.value })}
                required
              />
            </label>
            <label>
              Unit
              <input
                value={inventoryForm.quantityUnit}
                onChange={(event) => setInventoryForm({ ...inventoryForm, quantityUnit: event.target.value })}
                required
              />
            </label>
          </div>
          <div className="grid compact">
            <label>
              Purchase date
              <input
                type="date"
                value={inventoryForm.purchaseDate}
                onChange={(event) => setInventoryForm({ ...inventoryForm, purchaseDate: event.target.value })}
                required
              />
            </label>
            <label>
              Estimated expiry date
              <input
                type="date"
                value={inventoryForm.estimatedExpiryDate}
                onChange={(event) => setInventoryForm({ ...inventoryForm, estimatedExpiryDate: event.target.value })}
                required
              />
            </label>
          </div>
          <button type="submit">{editingId === null ? "Add item" : "Save changes"}</button>
        </form>

        <form onSubmit={submitFoodstuff} className="stack subtle-card">
          <h2>Quick-create foodstuff</h2>
          <p className="hint">Use this when no suitable suggestion exists. It becomes available for future items.</p>
          <label>
            Name
            <input value={foodstuffForm.name} onChange={(event) => setFoodstuffForm({ ...foodstuffForm, name: event.target.value })} required />
          </label>
          <label>
            Category
            <input
              value={foodstuffForm.category}
              onChange={(event) => setFoodstuffForm({ ...foodstuffForm, category: event.target.value })}
              required
            />
          </label>
          <div className="grid compact">
            <label>
              Min days
              <input
                type="number"
                min="0"
                value={foodstuffForm.expiryMinDays}
                onChange={(event) => setFoodstuffForm({ ...foodstuffForm, expiryMinDays: event.target.value })}
                required
              />
            </label>
            <label>
              Max days
              <input
                type="number"
                min="0"
                value={foodstuffForm.expiryMaxDays}
                onChange={(event) => setFoodstuffForm({ ...foodstuffForm, expiryMaxDays: event.target.value })}
                required
              />
            </label>
          </div>
          <button type="submit">Create foodstuff</button>
        </form>
      </section>

      <section className="panel stack">
        <div className="toolbar">
          <h2>Active inventory</h2>
          <div className="segmented" aria-label="Inventory view mode">
            <button className={viewMode === "expiry" ? "active" : ""} onClick={() => setViewMode("expiry")}>By expiry</button>
            <button className={viewMode === "category" ? "active" : ""} onClick={() => setViewMode("category")}>By category</button>
          </div>
        </div>
        {viewMode === "expiry" ? (
          <InventoryList items={items} onEdit={editItem} onRemove={removeItem} />
        ) : (
          <div className="stack">
            {groups.map((group) => (
              <section key={group.category} className="category-group">
                <h3>{group.category}</h3>
                <InventoryList items={group.items} onEdit={editItem} onRemove={removeItem} />
              </section>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

function InventoryList({
  items,
  onEdit,
  onRemove,
}: {
  items: InventoryItem[];
  onEdit: (item: InventoryItem) => void;
  onRemove: (item: InventoryItem) => void;
}) {
  if (items.length === 0) {
    return <p className="empty">No active inventory items yet.</p>;
  }
  return (
    <div className="cards">
      {items.map((item) => (
        <article key={item.id} className="item-card">
          <div>
            <h3>{item.name}</h3>
            <p>{item.quantity_amount} {item.quantity_unit} · {item.category}</p>
            <p className="hint">Purchased {item.purchase_date} · estimated expiry {item.estimated_expiry_date}</p>
          </div>
          <div className="card-actions">
            <button onClick={() => onEdit(item)}>Edit</button>
            <button className="secondary" onClick={() => onRemove(item)}>Remove</button>
          </div>
        </article>
      ))}
    </div>
  );
}

function addDays(dateValue: string, days: number): string {
  const date = new Date(`${dateValue}T00:00:00`);
  date.setDate(date.getDate() + days);
  return date.toISOString().slice(0, 10);
}
