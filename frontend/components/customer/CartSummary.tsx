'use client';

interface CartSummaryProps {
  totalAmount: number;
  itemCount: number;
}

export function CartSummary({ totalAmount, itemCount }: CartSummaryProps) {
  const formattedTotal = new Intl.NumberFormat('ko-KR').format(totalAmount);

  return (
    <div className="card mt-4">
      <div className="flex items-center justify-between">
        <span className="text-gray-600">총 {itemCount}개 항목</span>
        <span className="text-xl font-bold text-gray-900">{formattedTotal}원</span>
      </div>
    </div>
  );
}
