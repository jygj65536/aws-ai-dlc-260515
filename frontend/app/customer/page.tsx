'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { getAuthInfo } from '@/lib/auth';
import { MenuListResponse, MenuItem } from '@/types';
import { CategoryTabs } from '@/components/customer/CategoryTabs';
import { MenuGrid } from '@/components/customer/MenuGrid';
import { MenuDetailModal } from '@/components/customer/MenuDetailModal';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

interface CategoryWithItems {
  category_id: string;
  name: string;
  items: MenuItem[];
}

export default function CustomerMenuPage() {
  const [categories, setCategories] = useState<CategoryWithItems[]>([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(null);
  const [selectedMenu, setSelectedMenu] = useState<MenuItem | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchMenus = async () => {
    setIsLoading(true);
    setError('');
    try {
      const authInfo = getAuthInfo();
      if (!authInfo) return;

      const response = await api.get<MenuListResponse>(
        `/menus?store_id=${authInfo.store_id}`
      );
      setCategories(response.categories);
      if (response.categories.length > 0 && !selectedCategoryId) {
        setSelectedCategoryId(response.categories[0].category_id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '메뉴를 불러올 수 없습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMenus();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const filteredItems = selectedCategoryId
    ? categories.find((c) => c.category_id === selectedCategoryId)?.items ?? []
    : categories.flatMap((c) => c.items);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <ErrorMessage message={error} onRetry={fetchMenus} />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-4">
      <CategoryTabs
        categories={categories.map((c) => ({ id: c.category_id, name: c.name }))}
        selectedId={selectedCategoryId}
        onSelect={setSelectedCategoryId}
      />
      <MenuGrid items={filteredItems} onItemClick={setSelectedMenu} />
      <MenuDetailModal
        menu={selectedMenu}
        isOpen={selectedMenu !== null}
        onClose={() => setSelectedMenu(null)}
      />
    </div>
  );
}
