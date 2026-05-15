'use client';

import { useRouter } from 'next/navigation';
import { clearAuth } from '@/lib/auth';
import { Button } from '@/components/ui/Button';

interface AdminHeaderProps {
  storeName: string;
}

export function AdminHeader({ storeName }: AdminHeaderProps) {
  const router = useRouter();

  const handleLogout = () => {
    clearAuth();
    router.replace('/admin/login');
  };

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div className="text-sm text-gray-600">
        매장: <span className="font-medium text-gray-900">{storeName}</span>
      </div>
      <Button
        variant="secondary"
        size="sm"
        onClick={handleLogout}
        data-testid="admin-logout-button"
      >
        로그아웃
      </Button>
    </header>
  );
}
