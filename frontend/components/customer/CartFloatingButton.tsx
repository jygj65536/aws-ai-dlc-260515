'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { getCartItems, getCartItemCount } from '@/lib/cart';

export function CartFloatingButton() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const updateCount = () => {
      const items = getCartItems();
      setCount(getCartItemCount(items));
    };

    updateCount();

    // localStorage 변경 감지 (다른 탭에서 변경 시)
    window.addEventListener('storage', updateCount);
    // 커스텀 이벤트로 같은 탭 내 변경 감지
    window.addEventListener('cart-updated', updateCount);

    return () => {
      window.removeEventListener('storage', updateCount);
      window.removeEventListener('cart-updated', updateCount);
    };
  }, []);

  if (count === 0) return null;

  return (
    <Link
      href="/customer/cart"
      className="fixed bottom-6 right-6 bg-primary-600 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg hover:bg-primary-700 active:bg-primary-800 transition-colors z-50"
      data-testid="cart-floating-button"
      aria-label={`장바구니 ${count}개 항목`}
    >
      <div className="relative">
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"
          />
        </svg>
        <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
          {count > 99 ? '99+' : count}
        </span>
      </div>
    </Link>
  );
}
