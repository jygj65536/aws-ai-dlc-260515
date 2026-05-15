'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { Category, MenuItem } from '@/types';

interface MenuFormProps {
  categories: Category[];
  editingMenu: MenuItem | null;
  onSuccess: () => void;
  onCancel: () => void;
}

export function MenuForm({ categories, editingMenu, onSuccess, onCancel }: MenuFormProps) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [sortOrder, setSortOrder] = useState('0');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (editingMenu) {
      setName(editingMenu.name);
      setPrice(String(editingMenu.price));
      setDescription(editingMenu.description || '');
      setCategoryId(editingMenu.category_id);
      setSortOrder(String(editingMenu.sort_order));
    } else {
      setName('');
      setPrice('');
      setDescription('');
      setCategoryId(categories[0]?.category_id || '');
      setSortOrder('0');
    }
  }, [editingMenu, categories]);

  const validate = (): string | null => {
    if (!name || name.length > 50) return '메뉴명은 1~50자여야 합니다.';
    const priceNum = Number(price);
    if (!price || priceNum < 100 || priceNum > 1000000) return '가격은 100~1,000,000원이어야 합니다.';
    if (!categoryId) return '카테고리를 선택해주세요.';
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    const authInfo = getAuthInfo();
    if (!authInfo) return;

    setIsLoading(true);
    try {
      const body = {
        name,
        price: Number(price),
        description,
        category_id: categoryId,
        sort_order: Number(sortOrder),
      };

      if (editingMenu) {
        await api.put(`/menus/${editingMenu.menu_id}`, body);
      } else {
        await api.post('/menus', { ...body, store_id: authInfo.store_id });
      }

      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : '저장에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h3 className="font-semibold text-gray-900 mb-3">
        {editingMenu ? '메뉴 수정' : '메뉴 등록'}
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <Input
          label="메뉴명"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="메뉴명 (1~50자)"
          maxLength={50}
          data-testid="menu-form-name"
        />
        <Input
          label="가격 (원)"
          type="number"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          placeholder="100~1,000,000"
          min="100"
          max="1000000"
          data-testid="menu-form-price"
        />
        <div className="w-full">
          <label htmlFor="menu-category" className="block text-sm font-medium text-gray-700 mb-1">
            카테고리
          </label>
          <select
            id="menu-category"
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
            className="input-field"
            data-testid="menu-form-category"
          >
            <option value="">선택하세요</option>
            {categories.map((cat) => (
              <option key={cat.category_id} value={cat.category_id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="정렬 순서"
          type="number"
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
          placeholder="0"
          min="0"
          data-testid="menu-form-sort-order"
        />
        <div className="md:col-span-2">
          <Input
            label="설명"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="메뉴 설명 (선택)"
            data-testid="menu-form-description"
          />
        </div>
      </div>

      {error && <ErrorMessage message={error} className="mt-3" />}

      <div className="flex gap-2 mt-4">
        <Button type="submit" isLoading={isLoading} data-testid="menu-form-submit">
          {editingMenu ? '수정' : '등록'}
        </Button>
        {editingMenu && (
          <Button type="button" variant="secondary" onClick={onCancel} data-testid="menu-form-cancel">
            취소
          </Button>
        )}
      </div>
    </form>
  );
}
