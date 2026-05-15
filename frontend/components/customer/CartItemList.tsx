'use client';

import { CartItem as CartItemType } from '@/types';
import { CartItem } from './CartItem';

interface CartItemListProps {
  items: CartItemType[];
  onUpdateQuantity: (menuId: string, quantity: number) => void;
  onRemove: (menuId: string) => void;
}

export function CartItemList({ items, onUpdateQuantity, onRemove }: CartItemListProps) {
  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <svg className="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"
          />
        </svg>
        <p>장바구니가 비어있습니다.</p>
        <p className="text-sm mt-1">메뉴에서 원하는 항목을 추가해보세요.</p>
      </div>
    );
  }

  return (
    <div className="card">
      {items.map((item) => (
        <CartItem
          key={item.menu_id}
          item={item}
          onUpdateQuantity={onUpdateQuantity}
          onRemove={onRemove}
        />
      ))}
    </div>
  );
}
