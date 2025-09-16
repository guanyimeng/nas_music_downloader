import axios from "axios";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "");

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: false
});

// Attach token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Simple response error pass-through
api.interceptors.response.use(
  (res) => res,
  (err) => {
    return Promise.reject(err);
  }
);

// Auth endpoints
export async function login(username: string, password: string) {
  // FastAPI OAuth2PasswordRequestForm expects application/x-www-form-urlencoded
  const form = new URLSearchParams();
  form.set("username", username);
  form.set("password", password);
  // grant_type is optional in FastAPI; do not set to avoid conflicts unless required server-side
  const res = await api.post("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  });
  return res.data as { access_token: string; token_type: string };
}

export async function registerUser(data: { username: string; email: string; password: string }) {
  const res = await api.post("/auth/register", data);
  return res.data;
}

export async function me() {
  const res = await api.get("/auth/me");
  return res.data;
}

export async function logout() {
  const res = await api.post("/auth/logout");
  return res.data;
}

// Download endpoints
export async function requestDownload(url: string) {
  const res = await api.post("/api/download", { url });
  return res.data;
}

export async function listDownloads(page = 1, per_page = 10) {
  const res = await api.get("/api/downloads", { params: { page, per_page } });
  return res.data;
}

export async function getDownloadById(id: number) {
  const res = await api.get(`/api/downloads/${id}`);
  return res.data;
}
