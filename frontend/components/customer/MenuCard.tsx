'use client';

import { MenuItem } from '@/types';

interface MenuCardProps {
  menu: MenuItem;
  onClick: () => void;
}

export function MenuCard({ menu, onClick }: MenuCardProps) {
  const formattedPrice = new Intl.NumberFormat('ko-KR').format(menu.price);

  return (
    <button
      onClick={onClick}
      className="card text-left w-full hover:shadow-md active:shadow-sm transition-shadow"
      data-testid={`menu-card-${menu.menu_id}`}
    >
      <h3 className="font-semibold text-gray-900 text-sm line-clamp-2 mb-1">
        {menu.name}
      </h3>
      {menu.description && (
        <p className="text-xs text-gray-500 line-clamp-2 mb-2">{menu.description}</p>
      )}
      <p className="text-primary-600 font-bold text-sm">{formattedPrice}원</p>
    </button>
  );
}
