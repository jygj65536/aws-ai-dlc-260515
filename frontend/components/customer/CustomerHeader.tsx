'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface CustomerHeaderProps {
  tableNumber: number | null;
}

export function CustomerHeader({ tableNumber }: CustomerHeaderProps) {
  const pathname = usePathname();

  const navItems = [
    { href: '/customer', label: '메뉴', active: pathname === '/customer' },
    { href: '/customer/cart', label: '장바구니', active: pathname === '/customer/cart' },
    { href: '/customer/orders', label: '주문내역', active: pathname === '/customer/orders' },
  ];

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex items-center justify-between h-14">
          <div className="flex items-center gap-2">
            <span className="font-bold text-primary-600 text-lg">테이블오더</span>
            {tableNumber && (
              <span className="bg-primary-100 text-primary-700 text-sm font-medium px-2 py-0.5 rounded">
                {tableNumber}번
              </span>
            )}
          </div>
          <nav className="flex gap-1" aria-label="고객 메뉴">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                  item.active
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
                data-testid={`customer-nav-${item.label}`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
