'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { Category } from '@/types';

interface CategoryManagerProps {
  categories: Category[];
  onUpdate: () => void;
}

export function CategoryManager({ categories, onUpdate }: CategoryManagerProps) {
  const [newName, setNewName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) {
      setError('카테고리명을 입력해주세요.');
      return;
    }

    const authInfo = getAuthInfo();
    if (!authInfo) return;

    setIsLoading(true);
    setError('');
    try {
      await api.post('/categories', {
        store_id: authInfo.store_id,
        name: newName.trim(),
        sort_order: categories.length,
      });
      setNewName('');
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : '카테고리 추가에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (categoryId: string) => {
    if (!confirm('이 카테고리를 삭제하시겠습니까?')) return;
    try {
      await api.delete(`/categories/${categoryId}`);
      onUpdate();
    } catch (err) {
      alert(err instanceof Error ? err.message : '카테고리 삭제에 실패했습니다.');
    }
  };

  return (
    <div className="card">
      <h3 className="font-semibold text-gray-900 mb-3">카테고리 관리</h3>

      <form onSubmit={handleAdd} className="flex gap-2 mb-3">
        <Input
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="새 카테고리명"
          data-testid="category-name-input"
        />
        <Button type="submit" size="sm" isLoading={isLoading} data-testid="category-add-button">
          추가
        </Button>
      </form>

      {error && <ErrorMessage message={error} className="mb-3" />}

      <div className="space-y-2">
        {categories.map((cat) => (
          <div
            key={cat.category_id}
            className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-lg"
          >
            <span className="text-sm text-gray-700">{cat.name}</span>
            <button
              onClick={() => handleDelete(cat.category_id)}
              className="text-xs text-red-500 hover:text-red-700"
              data-testid={`category-delete-${cat.category_id}`}
            >
              삭제
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
