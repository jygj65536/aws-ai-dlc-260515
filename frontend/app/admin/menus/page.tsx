'use client';

import { useEffect, useState, useCallback } from 'react';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { Category, MenuItem, MenuListResponse } from '@/types';
import { MenuForm } from '@/components/admin/MenuForm';
import { CategoryManager } from '@/components/admin/CategoryManager';
import { MenuList } from '@/components/admin/MenuList';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

export default function MenusPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [menus, setMenus] = useState<MenuItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingMenu, setEditingMenu] = useState<MenuItem | null>(null);
  const [deleteMenuId, setDeleteMenuId] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      const authInfo = getAuthInfo();
      if (!authInfo) return;

      const [categoriesData, menusData] = await Promise.all([
        api.get<Category[]>(`/categories?store_id=${authInfo.store_id}`),
        api.get<MenuListResponse>(`/menus?store_id=${authInfo.store_id}`),
      ]);

      setCategories(categoriesData);
      setMenus(menusData.categories.flatMap((c) => c.items));
    } catch (err) {
      setError(err instanceof Error ? err.message : '데이터를 불러올 수 없습니다.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleMenuSuccess = () => {
    setEditingMenu(null);
    fetchData();
  };

  const handleDelete = async () => {
    if (!deleteMenuId) return;
    setIsDeleting(true);
    try {
      await api.delete(`/menus/${deleteMenuId}`);
      setDeleteMenuId(null);
      fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : '메뉴 삭제에 실패했습니다.');
    } finally {
      setIsDeleting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">메뉴 관리</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <MenuForm
            categories={categories}
            editingMenu={editingMenu}
            onSuccess={handleMenuSuccess}
            onCancel={() => setEditingMenu(null)}
          />

          <div>
            <h3 className="font-semibold text-gray-900 mb-3">등록된 메뉴</h3>
            <MenuList
              menus={menus}
              onEdit={setEditingMenu}
              onDelete={(id) => setDeleteMenuId(id)}
            />
          </div>
        </div>

        <div>
          <CategoryManager categories={categories} onUpdate={fetchData} />
        </div>
      </div>

      <ConfirmDialog
        isOpen={deleteMenuId !== null}
        onClose={() => setDeleteMenuId(null)}
        onConfirm={handleDelete}
        title="메뉴 삭제"
        message="이 메뉴를 삭제하시겠습니까? 삭제된 메뉴는 복구할 수 없습니다."
        confirmLabel="삭제"
        isLoading={isDeleting}
      />
    </div>
  );
}
