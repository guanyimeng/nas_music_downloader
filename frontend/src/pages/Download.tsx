import React, { useEffect, useMemo, useState } from "react";
import { requestDownload, listDownloads } from "../api/client";
import type { DownloadResponse } from "../types";

const POLL_INTERVAL_MS = 4000;

function StatusBadge({ status }: { status: DownloadResponse["status"] }) {
  const color = useMemo(() => {
    switch (status) {
      case "completed":
        return "#16a34a";
      case "downloading":
        return "#2563eb";
      case "failed":
        return "#dc2626";
      default:
        return "#a16207"; // pending
    }
  }, [status]);
  return (
    <span
      style={{
        background: color,
        color: "white",
        padding: "2px 8px",
        borderRadius: 999,
        fontSize: 12,
        textTransform: "capitalize"
      }}
    >
      {status}
    </span>
  );
}

export default function DownloadPage() {
  const [url, setUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  // show most recent 10 items, polling to reflect status changes
  const [items, setItems] = useState<DownloadResponse[]>([]);
  const [total, setTotal] = useState(0);

  const fetchLatest = async () => {
    try {
      const res = await listDownloads(1, 10);
      setItems(res.downloads);
      setTotal(res.total);
    } catch (e) {
      // ignore transient errors
    }
  };

  useEffect(() => {
    fetchLatest();
    const t = setInterval(fetchLatest, POLL_INTERVAL_MS);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    if (!url.trim()) return;
    setSubmitting(true);
    try {
      await requestDownload(url.trim());
      setMessage("Download queued successfully.");
      setUrl("");
      // immediate refresh after queuing
      fetchLatest();
    } catch (err: any) {
      const msg = err?.response?.data?.detail || "Failed to queue download";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2>Start a Download</h2>
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12, maxWidth: 720 }}>
        <label>
          <div>Media URL</div>
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            required
            style={{ width: "100%" }}
          />
        </label>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <button type="submit" disabled={submitting}>
            {submitting ? "Queuing..." : "Start Download"}
          </button>
          <button type="button" onClick={fetchLatest} disabled={submitting}>
            Refresh
          </button>
          <span style={{ color: "#666", fontSize: 13 }}>
            Total items in your history: {total}
          </span>
        </div>
        {error && <div style={{ color: "crimson" }}>{error}</div>}
        {message && <div style={{ color: "#155e75" }}>{message}</div>}
      </form>

      <h3 style={{ marginTop: 32 }}>Recent Activity</h3>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={th}>ID</th>
              <th style={th}>Title</th>
              <th style={th}>Artist</th>
              <th style={th}>URL</th>
              <th style={th}>Status</th>
              <th style={th}>File</th>
              <th style={th}>Created</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ padding: 12, textAlign: "center", color: "#666" }}>
                  No downloads yet.
                </td>
              </tr>
            ) : (
              items.map((d) => (
                <tr key={d.id}>
                  <td style={td}>{d.id}</td>
                  <td style={td}>{d.title || "-"}</td>
                  <td style={td}>{d.artist || "-"}</td>
                  <td style={{ ...td, maxWidth: 260, wordBreak: "break-all" }}>{d.url}</td>
                  <td style={td}>
                    <StatusBadge status={d.status} />
                  </td>
                  <td style={{ ...td, maxWidth: 260, wordBreak: "break-all" }}>
                    {d.file_path || "-"}
                  </td>
                  <td style={td}>{new Date(d.created_at).toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const th: React.CSSProperties = {
  textAlign: "left",
  borderBottom: "1px solid #e5e7eb",
  padding: "8px 12px",
  fontWeight: 600
};

const td: React.CSSProperties = {
  borderBottom: "1px solid #f1f5f9",
  padding: "8px 12px",
  verticalAlign: "top"
};
