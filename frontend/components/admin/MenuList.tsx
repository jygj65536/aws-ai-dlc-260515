'use client';

import { MenuItem } from '@/types';
import { MenuItemRow } from './MenuItemRow';

interface MenuListProps {
  menus: MenuItem[];
  onEdit: (menu: MenuItem) => void;
  onDelete: (menuId: string) => void;
}

export function MenuList({ menus, onEdit, onDelete }: MenuListProps) {
  if (menus.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>등록된 메뉴가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {menus.map((menu) => (
        <MenuItemRow
          key={menu.menu_id}
          menu={menu}
          onEdit={() => onEdit(menu)}
          onDelete={() => onDelete(menu.menu_id)}
        />
      ))}
    </div>
  );
}
