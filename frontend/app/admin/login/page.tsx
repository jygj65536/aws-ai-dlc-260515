'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getAuthInfo } from '@/lib/auth';
import { LoginForm } from '@/components/admin/LoginForm';

export default function AdminLoginPage() {
  const router = useRouter();

  useEffect(() => {
    const token = getToken();
    const authInfo = getAuthInfo();
    if (token && authInfo?.user_type === 'admin') {
      router.replace('/admin/dashboard');
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">관리자 로그인</h1>
          <p className="text-gray-500 mt-2">매장 관리 시스템에 로그인하세요</p>
        </div>
        <LoginForm />
      </div>
    </div>
  );
}
