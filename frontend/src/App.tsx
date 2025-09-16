import React from "react";
import { Routes, Route, Link, Navigate } from "react-router-dom";
import DownloadPage from "./pages/Download";
import HistoryPage from "./pages/History";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import { useAuth } from "./state/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

function Nav() {
  const { isAuthenticated, logout, user } = useAuth();
  return (
    <nav style={{ display: "flex", gap: 12, padding: 12, borderBottom: "1px solid #ddd" }}>
      <Link to="/">Download</Link>
      <Link to="/history">History</Link>
      <div style={{ marginLeft: "auto" }}>
        {isAuthenticated ? (
          <span style={{ display: "inline-flex", gap: 8, alignItems: "center" }}>
            <span>Hello, {user?.username}</span>
            <button onClick={logout}>Logout</button>
          </span>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register" style={{ marginLeft: 8 }}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <div>
      <Nav />
      <div style={{ padding: 16 }}>
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DownloadPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/history"
            element={
              <ProtectedRoute>
                <HistoryPage />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  );
}
