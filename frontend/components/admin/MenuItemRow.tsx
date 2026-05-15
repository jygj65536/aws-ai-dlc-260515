'use client';

import { MenuItem } from '@/types';
import { Button } from '@/components/ui/Button';

interface MenuItemRowProps {
  menu: MenuItem;
  onEdit: () => void;
  onDelete: () => void;
}

export function MenuItemRow({ menu, onEdit, onDelete }: MenuItemRowProps) {
  const formattedPrice = new Intl.NumberFormat('ko-KR').format(menu.price);

  return (
    <div
      className="flex items-center justify-between py-3 px-4 bg-white border border-gray-100 rounded-lg"
      data-testid={`menu-item-row-${menu.menu_id}`}
    >
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium text-gray-900 text-sm">{menu.name}</span>
          {!menu.is_available && (
            <span className="text-xs text-red-500 bg-red-50 px-1.5 py-0.5 rounded">품절</span>
          )}
        </div>
        <p className="text-xs text-gray-500 mt-0.5">{formattedPrice}원</p>
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="secondary"
          size="sm"
          onClick={onEdit}
          data-testid={`menu-edit-${menu.menu_id}`}
        >
          수정
        </Button>
        <Button
          variant="danger"
          size="sm"
          onClick={onDelete}
          data-testid={`menu-delete-${menu.menu_id}`}
        >
          삭제
        </Button>
      </div>
    </div>
  );
}
