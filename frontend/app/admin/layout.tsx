'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { getToken, getAuthInfo } from '@/lib/auth';
import { AdminSidebar } from '@/components/admin/AdminSidebar';
import { AdminHeader } from '@/components/admin/AdminHeader';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [isReady, setIsReady] = useState(false);
  const [storeName, setStoreName] = useState('');

  // 로그인 페이지는 레이아웃 적용 안 함
  const isLoginPage = pathname === '/admin/login';

  useEffect(() => {
    if (isLoginPage) {
      setIsReady(true);
      return;
    }

    const token = getToken();
    const authInfo = getAuthInfo();

    if (!token || !authInfo || authInfo.user_type !== 'admin') {
      router.replace('/admin/login');
      return;
    }

    setStoreName(authInfo.store_id);
    setIsReady(true);
  }, [router, isLoginPage]);

  if (!isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (isLoginPage) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <AdminSidebar />
      <div className="flex-1 flex flex-col ml-64">
        <AdminHeader storeName={storeName} />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
