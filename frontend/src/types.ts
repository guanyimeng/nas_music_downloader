export type TokenResponse = {
  access_token: string;
  token_type: string; // "bearer"
};

export type UserResponse = {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string; // ISO datetime
  last_login?: string | null;
};

export type DownloadRequest = {
  url: string;
};

export type DownloadResponse = {
  id: number;
  url: string;
  title?: string | null;
  artist?: string | null;
  status: "pending" | "downloading" | "completed" | "failed";
  file_path?: string | null;
  created_at: string; // ISO datetime
};

export type DownloadHistoryResponse = {
  downloads: DownloadResponse[];
  total: number;
  page: number;
  per_page: number;
};
