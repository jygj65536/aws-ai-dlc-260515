'use client';

import { Order } from '@/types';
import { Badge } from '@/components/ui/Badge';

interface TableCardProps {
  tableNumber: number;
  tableId: string;
  orders: Order[];
  totalAmount: number;
  isNew?: boolean;
  onClick: () => void;
}

export function TableCard({
  tableNumber,
  tableId,
  orders,
  totalAmount,
  isNew = false,
  onClick,
}: TableCardProps) {
  const formattedTotal = new Intl.NumberFormat('ko-KR').format(totalAmount);
  const pendingCount = orders.filter((o) => o.status === 'pending').length;

  return (
    <button
      onClick={onClick}
      className={`card text-left w-full hover:shadow-md transition-shadow ${
        isNew ? 'ring-2 ring-primary-400 animate-pulse' : ''
      }`}
      data-testid={`dashboard-table-card-${tableId}`}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="font-bold text-lg text-gray-900">{tableNumber}번</span>
        <div className="flex items-center gap-2">
          {pendingCount > 0 && (
            <Badge variant="warning">{pendingCount}건 대기</Badge>
          )}
        </div>
      </div>

      <div className="space-y-1 mb-3">
        {orders.slice(0, 3).map((order) => (
          <div key={order.order_id} className="text-xs text-gray-600 truncate">
            #{order.order_number} - {order.items.map((i) => i.name).join(', ')}
          </div>
        ))}
        {orders.length > 3 && (
          <p className="text-xs text-gray-400">외 {orders.length - 3}건</p>
        )}
      </div>

      <div className="border-t border-gray-100 pt-2">
        <span className="text-sm font-semibold text-gray-900">{formattedTotal}원</span>
      </div>
    </button>
  );
}
