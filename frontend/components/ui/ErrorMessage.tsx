'use client';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorMessage({ message, onRetry, className = '' }: ErrorMessageProps) {
  return (
    <div
      className={`flex flex-col items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-lg ${className}`}
      role="alert"
    >
      <div className="flex items-center gap-2 text-red-700">
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p className="text-sm font-medium">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-sm text-red-600 hover:text-red-800 underline"
          data-testid="error-retry-button"
        >
          다시 시도
        </button>
      )}
    </div>
  );
}
