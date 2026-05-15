'use client';

import { Order } from '@/types';
import { TableCard } from './TableCard';

interface TableData {
  tableId: string;
  tableNumber: number;
  orders: Order[];
  totalAmount: number;
  hasNewOrder: boolean;
}

interface TableGridProps {
  tables: TableData[];
  onTableClick: (tableId: string) => void;
}

export function TableGrid({ tables, onTableClick }: TableGridProps) {
  if (tables.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>현재 활성 주문이 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {tables.map((table) => (
        <TableCard
          key={table.tableId}
          tableId={table.tableId}
          tableNumber={table.tableNumber}
          orders={table.orders}
          totalAmount={table.totalAmount}
          isNew={table.hasNewOrder}
          onClick={() => onTableClick(table.tableId)}
        />
      ))}
    </div>
  );
}
