'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { api } from '@/lib/api';
import { saveToken, saveAuthInfo } from '@/lib/auth';
import { TableLoginResponse } from '@/types';

export default function CustomerSetupPage() {
  const router = useRouter();
  const [storeId, setStoreId] = useState('');
  const [tableNumber, setTableNumber] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!storeId || !tableNumber || !password) {
      setError('모든 필드를 입력해주세요.');
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.post<TableLoginResponse>('/auth/table/login', {
        store_id: storeId,
        table_number: Number(tableNumber),
        password,
      });

      saveToken(response.access_token);
      saveAuthInfo({
        user_type: 'table',
        store_id: storeId,
        table_id: response.table_id,
        session_id: response.session_id,
        table_number: Number(tableNumber),
      });

      router.replace('/customer');
    } catch (err) {
      setError(err instanceof Error ? err.message : '로그인에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">테이블 설정</h1>
          <p className="text-gray-500 mt-2">태블릿 초기 설정을 진행해주세요</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="매장 ID"
            value={storeId}
            onChange={(e) => setStoreId(e.target.value)}
            placeholder="매장 ID를 입력하세요"
            data-testid="setup-store-id-input"
          />
          <Input
            label="테이블 번호"
            type="number"
            value={tableNumber}
            onChange={(e) => setTableNumber(e.target.value)}
            placeholder="테이블 번호"
            min="1"
            max="999"
            data-testid="setup-table-number-input"
          />
          <Input
            label="비밀번호"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="비밀번호"
            data-testid="setup-password-input"
          />

          {error && <ErrorMessage message={error} />}

          <Button
            type="submit"
            className="w-full"
            isLoading={isLoading}
            data-testid="setup-submit-button"
          >
            설정 완료
          </Button>
        </form>
      </div>
    </div>
  );
}
