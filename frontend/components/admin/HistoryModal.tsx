'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { OrderHistory } from '@/types';
import { Modal } from '@/components/ui/Modal';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

interface HistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  tableId: string | null;
}

export function HistoryModal({ isOpen, onClose, tableId }: HistoryModalProps) {
  const [history, setHistory] = useState<OrderHistory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isOpen || !tableId) return;

    const fetchHistory = async () => {
      setIsLoading(true);
      setError('');
      try {
        const data = await api.get<OrderHistory[]>(`/tables/${tableId}/history`);
        setHistory(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : '내역을 불러올 수 없습니다.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, [isOpen, tableId]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="과거 주문 내역" size="lg">
      {isLoading && <LoadingSpinner className="py-8" />}
      {error && <ErrorMessage message={error} />}

      {!isLoading && !error && history.length === 0 && (
        <p className="text-center text-gray-500 py-8">과거 내역이 없습니다.</p>
      )}

      <div className="space-y-4 max-h-[60vh] overflow-y-auto">
        {history.map((entry) => (
          <div key={entry.history_id} className="border border-gray-100 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-500">
                {new Intl.DateTimeFormat('ko-KR', {
                  year: 'numeric',
                  month: '2-digit',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit',
                }).format(new Date(entry.completed_at))}
              </span>
              <span className="font-semibold text-gray-900">
                {new Intl.NumberFormat('ko-KR').format(entry.total_amount)}원
              </span>
            </div>
            <div className="space-y-1">
              {entry.orders.map((order, idx) => (
                <div key={idx} className="text-xs text-gray-600">
                  #{order.order_number}: {order.items.map((i) => `${i.name}×${i.quantity}`).join(', ')}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Modal>
  );
}
