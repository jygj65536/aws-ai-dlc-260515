'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { CartItem as CartItemType } from '@/types';
import {
  getCartItems,
  updateCartItemQuantity,
  removeCartItem,
  clearCart,
  getCartTotal,
  getCartItemCount,
} from '@/lib/cart';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { OrderCreateResponse } from '@/types';
import { CartItemList } from '@/components/customer/CartItemList';
import { CartSummary } from '@/components/customer/CartSummary';
import { OrderSuccessModal } from '@/components/customer/OrderSuccessModal';
import { Button } from '@/components/ui/Button';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

export default function CartPage() {
  const router = useRouter();
  const [items, setItems] = useState<CartItemType[]>([]);
  const [isOrdering, setIsOrdering] = useState(false);
  const [error, setError] = useState('');
  const [orderNumber, setOrderNumber] = useState<number | null>(null);

  useEffect(() => {
    setItems(getCartItems());
  }, []);

  const handleUpdateQuantity = (menuId: string, quantity: number) => {
    const updated = updateCartItemQuantity(menuId, quantity);
    setItems(updated);
    window.dispatchEvent(new Event('cart-updated'));
  };

  const handleRemove = (menuId: string) => {
    const updated = removeCartItem(menuId);
    setItems(updated);
    window.dispatchEvent(new Event('cart-updated'));
  };

  const handleOrder = async () => {
    const authInfo = getAuthInfo();
    if (!authInfo || !authInfo.table_id || !authInfo.session_id) {
      setError('인증 정보가 없습니다. 다시 로그인해주세요.');
      return;
    }

    setIsOrdering(true);
    setError('');

    try {
      const response = await api.post<OrderCreateResponse>('/orders', {
        store_id: authInfo.store_id,
        table_id: authInfo.table_id,
        session_id: authInfo.session_id,
        items: items.map((item) => ({
          menu_id: item.menu_id,
          name: item.name,
          quantity: item.quantity,
          price: item.price,
        })),
      });

      setOrderNumber(response.order_number);
      clearCart();
      window.dispatchEvent(new Event('cart-updated'));
    } catch (err) {
      setError(err instanceof Error ? err.message : '주문에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setIsOrdering(false);
    }
  };

  const handleOrderModalClose = () => {
    setOrderNumber(null);
    router.push('/customer');
  };

  const totalAmount = getCartTotal(items);
  const itemCount = getCartItemCount(items);

  return (
    <div className="max-w-4xl mx-auto px-4 py-4">
      <h1 className="text-xl font-bold text-gray-900 mb-4">장바구니</h1>

      <CartItemList
        items={items}
        onUpdateQuantity={handleUpdateQuantity}
        onRemove={handleRemove}
      />

      {items.length > 0 && (
        <>
          <CartSummary totalAmount={totalAmount} itemCount={itemCount} />

          {error && <ErrorMessage message={error} className="mt-4" />}

          <div className="mt-6">
            <Button
              onClick={handleOrder}
              className="w-full"
              size="lg"
              isLoading={isOrdering}
              data-testid="cart-order-button"
            >
              {new Intl.NumberFormat('ko-KR').format(totalAmount)}원 주문하기
            </Button>
          </div>
        </>
      )}

      <OrderSuccessModal
        isOpen={orderNumber !== null}
        orderNumber={orderNumber ?? 0}
        onClose={handleOrderModalClose}
      />
    </div>
  );
}
