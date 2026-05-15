'use client';

import { Table } from '@/types';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';

interface TableRowProps {
  table: Table;
  onDeleteOrder: (orderId: string) => void;
  onComplete: () => void;
  onViewHistory: () => void;
}

export function TableRow({ table, onComplete, onViewHistory }: TableRowProps) {
  const hasActiveSession = table.current_session_id !== null;

  return (
    <div className="card flex items-center justify-between" data-testid={`table-row-${table.table_id}`}>
      <div className="flex items-center gap-4">
        <span className="font-bold text-lg text-gray-900 w-16">
          {table.table_number}번
        </span>
        <Badge variant={hasActiveSession ? 'success' : 'default'}>
          {hasActiveSession ? '이용중' : '비어있음'}
        </Badge>
      </div>

      <div className="flex items-center gap-2">
        {hasActiveSession && (
          <Button
            variant="danger"
            size="sm"
            onClick={onComplete}
            data-testid={`table-complete-${table.table_id}`}
          >
            이용 완료
          </Button>
        )}
        <Button
          variant="secondary"
          size="sm"
          onClick={onViewHistory}
          data-testid={`table-history-${table.table_id}`}
        >
          과거 내역
        </Button>
      </div>
    </div>
  );
}
