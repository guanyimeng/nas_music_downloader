import React, { useEffect, useState } from "react";
import { listDownloads } from "../api/client";
import type { DownloadResponse } from "../types";

type PageData = {
  items: DownloadResponse[];
  total: number;
  page: number;
  per_page: number;
};

export default function HistoryPage() {
  const [data, setData] = useState<PageData>({ items: [], total: 0, page: 1, per_page: 10 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPage = async (page: number, perPage: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await listDownloads(page, perPage);
      setData({
        items: res.downloads,
        total: res.total,
        page: res.page,
        per_page: res.per_page
      });
    } catch (e: any) {
      const msg = e?.response?.data?.detail || "Failed to load history";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPage(1, data.per_page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const totalPages = Math.max(1, Math.ceil(data.total / data.per_page));
  const canPrev = data.page > 1;
  const canNext = data.page < totalPages;

  return (
    <div>
      <h2>Download History</h2>
      <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 12 }}>
        <button
          onClick={() => fetchPage(1, data.per_page)}
          disabled={loading}
          title="Reload"
        >
          Reload
        </button>
        <span style={{ color: "#666", fontSize: 13 }}>
          Total: {data.total} • Page {data.page} / {totalPages}
        </span>
        <div style={{ marginLeft: "auto", display: "flex", gap: 6 }}>
          <button onClick={() => canPrev && fetchPage(data.page - 1, data.per_page)} disabled={!canPrev || loading}>
            Prev
          </button>
          <button onClick={() => canNext && fetchPage(data.page + 1, data.per_page)} disabled={!canNext || loading}>
            Next
          </button>
          <select
            value={data.per_page}
            onChange={(e) => fetchPage(1, Number(e.target.value))}
            disabled={loading}
          >
            {[10, 20, 50].map((n) => (
              <option key={n} value={n}>
                {n} / page
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && <div style={{ color: "crimson", marginBottom: 12 }}>{error}</div>}
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
            {loading ? (
              <tr>
                <td colSpan={7} style={{ padding: 12 }}>Loading...</td>
              </tr>
            ) : data.items.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ padding: 12, textAlign: "center", color: "#666" }}>
                  No history.
                </td>
              </tr>
            ) : (
              data.items.map((d) => (
                <tr key={d.id}>
                  <td style={td}>{d.id}</td>
                  <td style={td}>{d.title || "-"}</td>
                  <td style={td}>{d.artist || "-"}</td>
                  <td style={{ ...td, maxWidth: 260, wordBreak: "break-all" }}>{d.url}</td>
                  <td style={td}>
                    <span
                      style={{
                        background: colorForStatus(d.status),
                        color: "white",
                        padding: "2px 8px",
                        borderRadius: 999,
                        fontSize: 12,
                        textTransform: "capitalize"
                      }}
                    >
                      {d.status}
                    </span>
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

function colorForStatus(status: DownloadResponse["status"]) {
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
