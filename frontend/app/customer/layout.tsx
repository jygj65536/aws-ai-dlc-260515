'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getAuthInfo } from '@/lib/auth';
import { CustomerHeader } from '@/components/customer/CustomerHeader';
import { CartFloatingButton } from '@/components/customer/CartFloatingButton';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

export default function CustomerLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [isReady, setIsReady] = useState(false);
  const [tableNumber, setTableNumber] = useState<number | null>(null);

  useEffect(() => {
    const token = getToken();
    const authInfo = getAuthInfo();

    if (!token || !authInfo || authInfo.user_type !== 'table') {
      router.replace('/customer/setup');
      return;
    }

    setTableNumber(authInfo.table_number ?? null);
    setIsReady(true);
  }, [router]);

  if (!isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <CustomerHeader tableNumber={tableNumber} />
      <main className="flex-1 pb-20">{children}</main>
      <CartFloatingButton />
    </div>
  );
}
