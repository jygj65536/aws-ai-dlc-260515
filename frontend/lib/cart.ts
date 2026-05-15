import { CartItem } from '@/types';

const CART_KEY = 'cart_items';

export function getCartItems(): CartItem[] {
  if (typeof window === 'undefined') return [];
  const raw = localStorage.getItem(CART_KEY);
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

export function saveCartItems(items: CartItem[]): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(CART_KEY, JSON.stringify(items));
}

export function addToCart(item: Omit<CartItem, 'quantity'>, quantity: number = 1): CartItem[] {
  const items = getCartItems();
  const existingIndex = items.findIndex((i) => i.menu_id === item.menu_id);

  if (existingIndex >= 0) {
    items[existingIndex].quantity += quantity;
  } else {
    items.push({ ...item, quantity });
  }

  saveCartItems(items);
  return items;
}

export function updateCartItemQuantity(menuId: string, quantity: number): CartItem[] {
  const items = getCartItems();
  const index = items.findIndex((i) => i.menu_id === menuId);

  if (index >= 0) {
    if (quantity <= 0) {
      items.splice(index, 1);
    } else {
      items[index].quantity = quantity;
    }
  }

  saveCartItems(items);
  return items;
}

export function removeCartItem(menuId: string): CartItem[] {
  const items = getCartItems().filter((i) => i.menu_id !== menuId);
  saveCartItems(items);
  return items;
}

export function clearCart(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(CART_KEY);
}

export function getCartTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function getCartItemCount(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.quantity, 0);
}
