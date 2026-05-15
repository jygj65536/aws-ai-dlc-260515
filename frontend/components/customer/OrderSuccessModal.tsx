'use client';

import { useEffect, useState } from 'react';
import { Modal } from '@/components/ui/Modal';

interface OrderSuccessModalProps {
  isOpen: boolean;
  orderNumber: number;
  onClose: () => void;
}

export function OrderSuccessModal({ isOpen, orderNumber, onClose }: OrderSuccessModalProps) {
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    if (!isOpen) {
      setCountdown(5);
      return;
    }

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          onClose();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isOpen, onClose]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="sm">
      <div className="text-center py-4">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 className="text-lg font-bold text-gray-900 mb-2">주문 완료!</h3>
        <p className="text-3xl font-bold text-primary-600 mb-2" data-testid="order-success-number">
          #{orderNumber}
        </p>
        <p className="text-sm text-gray-500">
          {countdown}초 후 메뉴 화면으로 이동합니다
        </p>
      </div>
    </Modal>
  );
}
