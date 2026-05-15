import { SSEEvent } from '@/types';
import { getToken } from './auth';

const MAX_RETRIES = 5;
const RETRY_DELAY = 3000;

interface SSEOptions {
  onEvent: (event: SSEEvent) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Event) => void;
}

export class SSEClient {
  private eventSource: EventSource | null = null;
  private retryCount = 0;
  private storeId: string;
  private options: SSEOptions;
  private isManualClose = false;

  constructor(storeId: string, options: SSEOptions) {
    this.storeId = storeId;
    this.options = options;
  }

  connect(): void {
    this.isManualClose = false;
    const token = getToken();
    const url = `/api/sse/orders/${this.storeId}${token ? `?token=${token}` : ''}`;

    this.eventSource = new EventSource(url);

    this.eventSource.onopen = () => {
      this.retryCount = 0;
      this.options.onConnect?.();
    };

    this.eventSource.addEventListener('new_order', (event) => {
      const data = JSON.parse(event.data);
      this.options.onEvent({ type: 'new_order', data });
    });

    this.eventSource.addEventListener('order_updated', (event) => {
      const data = JSON.parse(event.data);
      this.options.onEvent({ type: 'order_updated', data });
    });

    this.eventSource.addEventListener('order_deleted', (event) => {
      const data = JSON.parse(event.data);
      this.options.onEvent({ type: 'order_deleted', data });
    });

    this.eventSource.onerror = (error) => {
      this.options.onError?.(error);
      this.options.onDisconnect?.();

      if (this.isManualClose) return;

      this.eventSource?.close();
      this.eventSource = null;

      if (this.retryCount < MAX_RETRIES) {
        this.retryCount++;
        setTimeout(() => this.connect(), RETRY_DELAY);
      }
    };
  }

  disconnect(): void {
    this.isManualClose = true;
    this.eventSource?.close();
    this.eventSource = null;
  }

  get isConnected(): boolean {
    return this.eventSource?.readyState === EventSource.OPEN;
  }
}
