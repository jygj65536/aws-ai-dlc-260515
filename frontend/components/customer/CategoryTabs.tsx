'use client';

interface CategoryTabsProps {
  categories: Array<{ id: string; name: string }>;
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function CategoryTabs({ categories, selectedId, onSelect }: CategoryTabsProps) {
  if (categories.length === 0) return null;

  return (
    <div
      className="flex gap-2 overflow-x-auto pb-3 mb-4 scrollbar-hide"
      role="tablist"
      aria-label="메뉴 카테고리"
    >
      {categories.map((category) => (
        <button
          key={category.id}
          role="tab"
          aria-selected={selectedId === category.id}
          onClick={() => onSelect(category.id)}
          className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors whitespace-nowrap ${
            selectedId === category.id
              ? 'bg-primary-600 text-white'
              : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
          }`}
          data-testid={`category-tab-${category.id}`}
        >
          {category.name}
        </button>
      ))}
    </div>
  );
}
