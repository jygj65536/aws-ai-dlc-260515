// ===== Store =====
export interface Store {
  store_id: string;
  name: string;
  created_at: string;
}

// ===== Auth =====
export interface AdminLoginRequest {
  store_id: string;
  username: string;
  password: string;
}

export interface AdminLoginResponse {
  access_token: string;
  token_type: string;
}

export interface TableLoginRequest {
  store_id: string;
  table_number: number;
  password: string;
}

export interface TableLoginResponse {
  access_token: string;
  table_id: string;
  session_id: string;
}

export interface AuthInfo {
  user_type: 'admin' | 'table';
  store_id: string;
  username?: string;
  table_id?: string;
  session_id?: string;
  table_number?: number;
}

// ===== Table =====
export interface Table {
  table_id: string;
  store_id: string;
  table_number: number;
  current_session_id: string | null;
  session_status?: string;
  created_at: string;
}

export interface TableCreateRequest {
  store_id: string;
  table_number: number;
  password: string;
}

// ===== TableSession =====
export interface TableSession {
  table_id: string;
  session_id: string;
  store_id: string;
  status: 'active' | 'expired' | 'completed';
  started_at: string;
  expires_at: string;
  completed_at: string | null;
  total_amount: number;
}

// ===== Category =====
export interface Category {
  category_id: string;
  store_id: string;
  name: string;
  sort_order: number;
  created_at: string;
}

export interface CategoryCreateRequest {
  store_id: string;
  name: string;
  sort_order: number;
}

export interface CategoryUpdateRequest {
  name: string;
  sort_order: number;
}

// ===== MenuItem =====
export interface MenuItem {
  menu_id: string;
  store_id: string;
  category_id: string;
  name: string;
  price: number;
  description: string;
  image_url: string | null;
  sort_order: number;
  is_available: boolean;
  created_at: string;
}

export interface MenuCreateRequest {
  store_id: string;
  name: string;
  price: number;
  description: string;
  category_id: string;
  sort_order: number;
}

export interface MenuUpdateRequest {
  name: string;
  price: number;
  description: string;
  category_id: string;
  sort_order: number;
}

export interface MenuListResponse {
  categories: Array<{
    category_id: string;
    name: string;
    sort_order: number;
    items: MenuItem[];
  }>;
}

// ===== Order =====
export interface OrderItem {
  menu_id: string;
  name: string;
  quantity: number;
  price: number;
  subtotal: number;
}

export interface Order {
  order_id: string;
  session_id: string;
  store_id: string;
  table_id: string;
  order_number: number;
  status: 'pending' | 'preparing' | 'completed';
  items: OrderItem[];
  total_amount: number;
  created_at: string;
}

export interface OrderCreateRequest {
  store_id: string;
  table_id: string;
  session_id: string;
  items: Array<{
    menu_id: string;
    name: string;
    quantity: number;
    price: number;
  }>;
}

export interface OrderCreateResponse {
  order_id: string;
  order_number: number;
  total_amount: number;
  session_id: string;
}

export interface OrderStatusUpdateRequest {
  status: 'preparing' | 'completed';
}

// ===== OrderHistory =====
export interface OrderHistory {
  history_id: string;
  table_id: string;
  store_id: string;
  session_id: string;
  orders: Order[];
  total_amount: number;
  completed_at: string;
}

// ===== Cart (Client-side) =====
export interface CartItem {
  menu_id: string;
  name: string;
  price: number;
  quantity: number;
}

// ===== SSE Events =====
export interface SSENewOrderEvent {
  type: 'new_order';
  data: Order;
}

export interface SSEOrderUpdatedEvent {
  type: 'order_updated';
  data: {
    order_id: string;
    status: Order['status'];
  };
}

export interface SSEOrderDeletedEvent {
  type: 'order_deleted';
  data: {
    order_id: string;
  };
}

export type SSEEvent = SSENewOrderEvent | SSEOrderUpdatedEvent | SSEOrderDeletedEvent;

// ===== API Response =====
export interface ApiError {
  detail: string;
}

export interface SuccessResponse {
  success: boolean;
  message?: string;
}
