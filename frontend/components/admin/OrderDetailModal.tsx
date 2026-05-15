'use client';

import { Order } from '@/types';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { StatusBadge } from '@/components/customer/StatusBadge';

interface OrderDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  tableNumber: number;
  orders: Order[];
  onStatusChange: (orderId: string, status: 'preparing' | 'completed') => void;
}

export function OrderDetailModal({
  isOpen,
  onClose,
  tableNumber,
  orders,
  onStatusChange,
}: OrderDetailModalProps) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`${tableNumber}번 테이블 주문`} size="lg">
      <div className="space-y-4 max-h-[60vh] overflow-y-auto">
        {orders.map((order) => (
          <div key={order.order_id} className="border border-gray-100 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="font-bold text-gray-900">#{order.order_number}</span>
                <span className="text-xs text-gray-500">
                  {new Intl.DateTimeFormat('ko-KR', {
                    hour: '2-digit',
                    minute: '2-digit',
                  }).format(new Date(order.created_at))}
                </span>
              </div>
              <StatusBadge status={order.status} />
            </div>

            <div className="space-y-1 mb-3">
              {order.items.map((item, idx) => (
                <div key={idx} className="flex justify-between text-sm">
                  <span className="text-gray-700">
                    {item.name} × {item.quantity}
                  </span>
                  <span className="text-gray-500">
                    {new Intl.NumberFormat('ko-KR').format(item.subtotal)}원
                  </span>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between border-t border-gray-100 pt-2">
              <span className="font-semibold text-sm">
                {new Intl.NumberFormat('ko-KR').format(order.total_amount)}원
              </span>
              <div className="flex gap-2">
                {order.status === 'pending' && (
                  <Button
                    size="sm"
                    onClick={() => onStatusChange(order.order_id, 'preparing')}
                    data-testid={`order-status-preparing-${order.order_id}`}
                  >
                    준비 시작
                  </Button>
                )}
                {order.status === 'preparing' && (
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => onStatusChange(order.order_id, 'completed')}
                    data-testid={`order-status-completed-${order.order_id}`}
                  >
                    완료
                  </Button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </Modal>
  );
}
