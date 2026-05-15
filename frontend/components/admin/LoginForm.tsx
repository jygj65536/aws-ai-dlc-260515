'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { api } from '@/lib/api';
import { saveToken, saveAuthInfo } from '@/lib/auth';
import { AdminLoginResponse } from '@/types';

export function LoginForm() {
  const router = useRouter();
  const [storeId, setStoreId] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!storeId || !username || !password) {
      setError('모든 필드를 입력해주세요.');
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.post<AdminLoginResponse>('/auth/admin/login', {
        store_id: storeId,
        username,
        password,
      });

      saveToken(response.access_token);
      saveAuthInfo({
        user_type: 'admin',
        store_id: storeId,
        username,
      });

      router.replace('/admin/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : '로그인에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="매장 ID"
        value={storeId}
        onChange={(e) => setStoreId(e.target.value)}
        placeholder="매장 ID"
        data-testid="admin-login-store-id"
      />
      <Input
        label="사용자명"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="사용자명"
        data-testid="admin-login-username"
      />
      <Input
        label="비밀번호"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="비밀번호"
        data-testid="admin-login-password"
      />

      {error && <ErrorMessage message={error} />}

      <Button
        type="submit"
        className="w-full"
        isLoading={isLoading}
        data-testid="admin-login-submit"
      >
        로그인
      </Button>
    </form>
  );
}
