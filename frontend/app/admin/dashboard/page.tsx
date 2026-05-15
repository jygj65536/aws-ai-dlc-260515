'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { Order, SSEEvent, Table } from '@/types';
import { SSEClient } from '@/lib/sse';
import { TableGrid } from '@/components/admin/TableGrid';
import { OrderDetailModal } from '@/components/admin/OrderDetailModal';
import { Badge } from '@/components/ui/Badge';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

interface TableData {
  tableId: string;
  tableNumber: number;
  orders: Order[];
  totalAmount: number;
  hasNewOrder: boolean;
}

export default function DashboardPage() {
  const [tables, setTables] = useState<TableData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [sseConnected, setSseConnected] = useState(false);
  const [selectedTableId, setSelectedTableId] = useState<string | null>(null);
  const sseClientRef = useRef<SSEClient | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const authInfo = getAuthInfo();
      if (!authInfo) return;

      const [tablesData, ordersData] = await Promise.all([
        api.get<Table[]>(`/tables?store_id=${authInfo.store_id}`),
        api.get<Order[]>(`/orders?store_id=${authInfo.store_id}`),
      ]);

      const tableMap = new Map<string, TableData>();
      tablesData.forEach((t) => {
        tableMap.set(t.table_id, {
          tableId: t.table_id,
          tableNumber: t.table_number,
          orders: [],
          totalAmount: 0,
          hasNewOrder: false,
        });
      });

      ordersData.forEach((order) => {
        const table = tableMap.get(order.table_id);
        if (table) {
          table.orders.push(order);
          table.totalAmount += order.total_amount;
        }
      });

      setTables(Array.from(tableMap.values()).filter((t) => t.orders.length > 0));
    } catch (err) {
      setError(err instanceof Error ? err.message : '데이터를 불러올 수 없습니다.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleSSEEvent = useCallback((event: SSEEvent) => {
    switch (event.type) {
      case 'new_order': {
        const order = event.data;
        setTables((prev) => {
          const existing = prev.find((t) => t.tableId === order.table_id);
          if (existing) {
            return prev.map((t) =>
              t.tableId === order.table_id
                ? {
                    ...t,
                    orders: [...t.orders, order],
                    totalAmount: t.totalAmount + order.total_amount,
                    hasNewOrder: true,
                  }
                : t
            );
          }
          return [
            ...prev,
            {
              tableId: order.table_id,
              tableNumber: 0, // 새 테이블은 다음 fetch에서 업데이트
              orders: [order],
              totalAmount: order.total_amount,
              hasNewOrder: true,
            },
          ];
        });
        // 3초 후 하이라이트 제거
        setTimeout(() => {
          setTables((prev) =>
            prev.map((t) =>
              t.tableId === order.table_id ? { ...t, hasNewOrder: false } : t
            )
          );
        }, 3000);
        break;
      }
      case 'order_updated': {
        const { order_id, status } = event.data;
        setTables((prev) =>
          prev.map((t) => ({
            ...t,
            orders: t.orders.map((o) =>
              o.order_id === order_id ? { ...o, status } : o
            ),
          }))
        );
        break;
      }
      case 'order_deleted': {
        const { order_id } = event.data;
        setTables((prev) =>
          prev
            .map((t) => {
              const deletedOrder = t.orders.find((o) => o.order_id === order_id);
              return {
                ...t,
                orders: t.orders.filter((o) => o.order_id !== order_id),
                totalAmount: t.totalAmount - (deletedOrder?.total_amount ?? 0),
              };
            })
            .filter((t) => t.orders.length > 0)
        );
        break;
      }
    }
  }, []);

  useEffect(() => {
    fetchData();

    const authInfo = getAuthInfo();
    if (authInfo) {
      const client = new SSEClient(authInfo.store_id, {
        onEvent: handleSSEEvent,
        onConnect: () => setSseConnected(true),
        onDisconnect: () => setSseConnected(false),
      });
      client.connect();
      sseClientRef.current = client;
    }

    return () => {
      sseClientRef.current?.disconnect();
    };
  }, [fetchData, handleSSEEvent]);

  const handleStatusChange = async (orderId: string, status: 'preparing' | 'completed', sessionId?: string) => {
    try {
      const sid = sessionId || tables.flatMap(t => t.orders).find(o => o.order_id === orderId)?.session_id;
      await api.patch(`/orders/${orderId}/status?session_id=${sid}`, { status });
      setTables((prev) =>
        prev.map((t) => ({
          ...t,
          orders: t.orders.map((o) =>
            o.order_id === orderId ? { ...o, status } : o
          ),
        }))
      );
    } catch (err) {
      alert(err instanceof Error ? err.message : '상태 변경에 실패했습니다.');
    }
  };

  const selectedTable = tables.find((t) => t.tableId === selectedTableId);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">주문 모니터링</h1>
        <Badge variant={sseConnected ? 'success' : 'danger'}>
          {sseConnected ? '실시간 연결됨' : '연결 끊김'}
        </Badge>
      </div>

      <TableGrid tables={tables} onTableClick={setSelectedTableId} />

      {selectedTable && (
        <OrderDetailModal
          isOpen={selectedTableId !== null}
          onClose={() => setSelectedTableId(null)}
          tableNumber={selectedTable.tableNumber}
          orders={selectedTable.orders}
          onStatusChange={handleStatusChange}
        />
      )}
    </div>
  );
}
