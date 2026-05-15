'use client';

import { Table } from '@/types';
import { TableRow } from './TableRow';

interface TableListProps {
  tables: Table[];
  onDeleteOrder: (orderId: string) => void;
  onComplete: (tableId: string) => void;
  onViewHistory: (tableId: string) => void;
}

export function TableList({ tables, onDeleteOrder, onComplete, onViewHistory }: TableListProps) {
  if (tables.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>등록된 테이블이 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tables.map((table) => (
        <TableRow
          key={table.table_id}
          table={table}
          onDeleteOrder={onDeleteOrder}
          onComplete={() => onComplete(table.table_id)}
          onViewHistory={() => onViewHistory(table.table_id)}
        />
      ))}
    </div>
  );
}
