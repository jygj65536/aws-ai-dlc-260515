'use client';

import { useEffect, useState, useCallback } from 'react';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { Table } from '@/types';
import { TableSetupForm } from '@/components/admin/TableSetupForm';
import { TableList } from '@/components/admin/TableList';
import { HistoryModal } from '@/components/admin/HistoryModal';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

export default function TablesPage() {
  const [tables, setTables] = useState<Table[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [historyTableId, setHistoryTableId] = useState<string | null>(null);
  const [completeTableId, setCompleteTableId] = useState<string | null>(null);
  const [isCompleting, setIsCompleting] = useState(false);

  const fetchTables = useCallback(async () => {
    try {
      const authInfo = getAuthInfo();
      if (!authInfo) return;
      const data = await api.get<Table[]>(`/tables?store_id=${authInfo.store_id}`);
      setTables(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '테이블 목록을 불러올 수 없습니다.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTables();
  }, [fetchTables]);

  const handleComplete = async () => {
    if (!completeTableId) return;
    setIsCompleting(true);
    try {
      await api.post(`/tables/${completeTableId}/complete`);
      setCompleteTableId(null);
      fetchTables();
    } catch (err) {
      alert(err instanceof Error ? err.message : '이용 완료 처리에 실패했습니다.');
    } finally {
      setIsCompleting(false);
    }
  };

  const handleDeleteOrder = async (orderId: string) => {
    if (!confirm('이 주문을 삭제하시겠습니까?')) return;
    try {
      await api.delete(`/orders/${orderId}`);
      fetchTables();
    } catch (err) {
      alert(err instanceof Error ? err.message : '주문 삭제에 실패했습니다.');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchTables} />;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">테이블 관리</h1>

      <TableSetupForm onSuccess={fetchTables} />

      <div className="mt-6">
        <TableList
          tables={tables}
          onDeleteOrder={handleDeleteOrder}
          onComplete={(tableId) => setCompleteTableId(tableId)}
          onViewHistory={(tableId) => setHistoryTableId(tableId)}
        />
      </div>

      <HistoryModal
        isOpen={historyTableId !== null}
        onClose={() => setHistoryTableId(null)}
        tableId={historyTableId}
      />

      <ConfirmDialog
        isOpen={completeTableId !== null}
        onClose={() => setCompleteTableId(null)}
        onConfirm={handleComplete}
        title="이용 완료"
        message="이 테이블의 이용을 완료하시겠습니까? 주문 내역이 과거 이력으로 이동됩니다."
        confirmLabel="이용 완료"
        isLoading={isCompleting}
      />
    </div>
  );
}
