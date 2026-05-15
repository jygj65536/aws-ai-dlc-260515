'use client';

import { Order } from '@/types';
import { StatusBadge } from './StatusBadge';

interface OrderCardProps {
  order: Order;
}

export function OrderCard({ order }: OrderCardProps) {
  const formattedTotal = new Intl.NumberFormat('ko-KR').format(order.total_amount);
  const formattedTime = new Intl.DateTimeFormat('ko-KR', {
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(order.created_at));

  return (
    <div className="card" data-testid={`order-card-${order.order_id}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="font-bold text-gray-900">#{order.order_number}</span>
          <span className="text-xs text-gray-500">{formattedTime}</span>
        </div>
        <StatusBadge status={order.status} />
      </div>

      <div className="space-y-1 mb-3">
        {order.items.map((item, index) => (
          <div key={index} className="flex justify-between text-sm">
            <span className="text-gray-700">
              {item.name} × {item.quantity}
            </span>
            <span className="text-gray-500">
              {new Intl.NumberFormat('ko-KR').format(item.subtotal)}원
            </span>
          </div>
        ))}
      </div>

      <div className="border-t border-gray-100 pt-2 flex justify-end">
        <span className="font-semibold text-gray-900">{formattedTotal}원</span>
      </div>
    </div>
  );
}
