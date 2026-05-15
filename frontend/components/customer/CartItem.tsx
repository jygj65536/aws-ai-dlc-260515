'use client';

import { CartItem as CartItemType } from '@/types';

interface CartItemProps {
  item: CartItemType;
  onUpdateQuantity: (menuId: string, quantity: number) => void;
  onRemove: (menuId: string) => void;
}

export function CartItem({ item, onUpdateQuantity, onRemove }: CartItemProps) {
  const formattedPrice = new Intl.NumberFormat('ko-KR').format(item.price);
  const formattedSubtotal = new Intl.NumberFormat('ko-KR').format(item.price * item.quantity);

  return (
    <div className="flex items-center gap-3 py-3 border-b border-gray-100 last:border-0">
      <div className="flex-1 min-w-0">
        <h4 className="font-medium text-gray-900 text-sm truncate">{item.name}</h4>
        <p className="text-xs text-gray-500">{formattedPrice}원</p>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => onUpdateQuantity(item.menu_id, item.quantity - 1)}
          className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center text-gray-600 hover:bg-gray-50 text-sm"
          data-testid={`cart-item-decrease-${item.menu_id}`}
          aria-label={`${item.name} 수량 감소`}
        >
          −
        </button>
        <span className="text-sm font-semibold w-6 text-center">{item.quantity}</span>
        <button
          onClick={() => onUpdateQuantity(item.menu_id, item.quantity + 1)}
          className="w-7 h-7 rounded-full border border-gray-300 flex items-center justify-center text-gray-600 hover:bg-gray-50 text-sm"
          data-testid={`cart-item-increase-${item.menu_id}`}
          aria-label={`${item.name} 수량 증가`}
        >
          +
        </button>
      </div>

      <div className="text-right min-w-[70px]">
        <p className="text-sm font-semibold text-gray-900">{formattedSubtotal}원</p>
      </div>

      <button
        onClick={() => onRemove(item.menu_id)}
        className="p-1 text-gray-400 hover:text-red-500"
        data-testid={`cart-item-remove-${item.menu_id}`}
        aria-label={`${item.name} 삭제`}
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
}
