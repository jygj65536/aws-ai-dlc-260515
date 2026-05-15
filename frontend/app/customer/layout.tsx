'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
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
  const pathname = usePathname();
  const [authState, setAuthState] = useState<'loading' | 'authenticated' | 'unauthenticated'>('loading');
  const [tableNumber, setTableNumber] = useState<number | null>(null);

  useEffect(() => {
    // setup 페이지는 인증 불필요
    if (pathname === '/customer/setup') {
      setAuthState('authenticated');
      return;
    }

    // localStorage에서 인증 정보 확인
    const token = getToken();
    const authInfo = getAuthInfo();

    if (token && authInfo && authInfo.user_type === 'table') {
      setTableNumber(authInfo.table_number ?? null);
      setAuthState('authenticated');
    } else {
      setAuthState('unauthenticated');
    }
  }, [pathname]);

  // 미인증 시 setup으로 리다이렉트 (useEffect 분리하여 무한 루프 방지)
  useEffect(() => {
    if (authState === 'unauthenticated' && pathname !== '/customer/setup') {
      router.replace('/customer/setup');
    }
  }, [authState, pathname, router]);

  // setup 페이지는 레이아웃 없이 바로 렌더
  if (pathname === '/customer/setup') {
    return <>{children}</>;
  }

  if (authState === 'loading' || authState === 'unauthenticated') {
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
