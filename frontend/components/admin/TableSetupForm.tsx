'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';

interface TableSetupFormProps {
  onSuccess: () => void;
}

export function TableSetupForm({ onSuccess }: TableSetupFormProps) {
  const [tableNumber, setTableNumber] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const num = Number(tableNumber);
    if (!tableNumber || num < 1 || num > 999) {
      setError('테이블 번호는 1~999 사이여야 합니다.');
      return;
    }
    if (!password || password.length < 4 || password.length > 20) {
      setError('비밀번호는 4~20자여야 합니다.');
      return;
    }

    const authInfo = getAuthInfo();
    if (!authInfo) return;

    setIsLoading(true);
    try {
      await api.post('/tables', {
        store_id: authInfo.store_id,
        table_number: num,
        password,
      });
      setTableNumber('');
      setPassword('');
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : '테이블 생성에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h3 className="font-semibold text-gray-900 mb-3">새 테이블 추가</h3>
      <div className="flex gap-3 items-end">
        <Input
          label="테이블 번호"
          type="number"
          value={tableNumber}
          onChange={(e) => setTableNumber(e.target.value)}
          placeholder="1~999"
          min="1"
          max="999"
          data-testid="table-setup-number-input"
        />
        <Input
          label="비밀번호"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="4~20자"
          data-testid="table-setup-password-input"
        />
        <Button
          type="submit"
          isLoading={isLoading}
          data-testid="table-setup-submit"
        >
          추가
        </Button>
      </div>
      {error && <ErrorMessage message={error} className="mt-3" />}
    </form>
  );
}
