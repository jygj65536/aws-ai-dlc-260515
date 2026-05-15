'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { Order } from '@/types';
import { OrderCard } from '@/components/customer/OrderCard';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchOrders = async () => {
    setIsLoading(true);
    setError('');
    try {
      const authInfo = getAuthInfo();
      if (!authInfo?.session_id) return;

      const data = await api.get<Order[]>(
        `/orders?session_id=${authInfo.session_id}`
      );
      setOrders(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '주문 내역을 불러올 수 없습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <ErrorMessage message={error} onRetry={fetchOrders} />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-4">
      <h1 className="text-xl font-bold text-gray-900 mb-4">주문 내역</h1>

      {orders.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>아직 주문 내역이 없습니다.</p>
          <p className="text-sm mt-1">메뉴에서 주문을 시작해보세요.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {orders.map((order) => (
            <OrderCard key={order.order_id} order={order} />
          ))}
        </div>
      )}
    </div>
  );
}
