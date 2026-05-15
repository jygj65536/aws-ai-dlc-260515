'use client';

import { MenuItem } from '@/types';
import { MenuCard } from './MenuCard';

interface MenuGridProps {
  items: MenuItem[];
  onItemClick: (item: MenuItem) => void;
}

export function MenuGrid({ items, onItemClick }: MenuGridProps) {
  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>등록된 메뉴가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
      {items
        .filter((item) => item.is_available)
        .map((item) => (
          <MenuCard key={item.menu_id} menu={item} onClick={() => onItemClick(item)} />
        ))}
    </div>
  );
}
