'use client';

import { useState } from 'react';
import { MenuItem } from '@/types';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { addToCart } from '@/lib/cart';

interface MenuDetailModalProps {
  menu: MenuItem | null;
  isOpen: boolean;
  onClose: () => void;
}

export function MenuDetailModal({ menu, isOpen, onClose }: MenuDetailModalProps) {
  const [quantity, setQuantity] = useState(1);

  if (!menu) return null;

  const formattedPrice = new Intl.NumberFormat('ko-KR').format(menu.price);
  const formattedTotal = new Intl.NumberFormat('ko-KR').format(menu.price * quantity);

  const handleAdd = () => {
    addToCart(
      { menu_id: menu.menu_id, name: menu.name, price: menu.price },
      quantity
    );
    window.dispatchEvent(new Event('cart-updated'));
    setQuantity(1);
    onClose();
  };

  const handleClose = () => {
    setQuantity(1);
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title={menu.name} size="sm">
      <div className="space-y-4">
        <div>
          <p className="text-lg font-bold text-primary-600">{formattedPrice}원</p>
          {menu.description && (
            <p className="text-gray-600 mt-2">{menu.description}</p>
          )}
        </div>

        <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3">
          <span className="text-sm font-medium text-gray-700">수량</span>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setQuantity(Math.max(1, quantity - 1))}
              className="w-8 h-8 rounded-full bg-white border border-gray-300 flex items-center justify-center text-gray-600 hover:bg-gray-50"
              data-testid="menu-detail-decrease-qty"
              aria-label="수량 감소"
            >
              −
            </button>
            <span className="text-lg font-semibold w-8 text-center">{quantity}</span>
            <button
              onClick={() => setQuantity(quantity + 1)}
              className="w-8 h-8 rounded-full bg-white border border-gray-300 flex items-center justify-center text-gray-600 hover:bg-gray-50"
              data-testid="menu-detail-increase-qty"
              aria-label="수량 증가"
            >
              +
            </button>
          </div>
        </div>

        <Button
          onClick={handleAdd}
          className="w-full"
          data-testid="menu-detail-add-to-cart"
        >
          {formattedTotal}원 담기
        </Button>
      </div>
    </Modal>
  );
}
