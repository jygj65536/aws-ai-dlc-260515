'use client';

import { Badge } from '@/components/ui/Badge';

interface StatusBadgeProps {
  status: 'pending' | 'preparing' | 'completed';
}

const statusConfig = {
  pending: { label: '대기중', variant: 'warning' as const },
  preparing: { label: '준비중', variant: 'info' as const },
  completed: { label: '완료', variant: 'success' as const },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];
  return <Badge variant={config.variant}>{config.label}</Badge>;
}
