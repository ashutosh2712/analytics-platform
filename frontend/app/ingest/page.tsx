"use client";

import { useMemo, useState } from "react";

import { Upload, Send, Copy, Database } from "lucide-react";

import api from "@/lib/api";

import { isOwner, isAdmin } from "@/lib/auth";
import Navbar from "@/components/Navbar";

const IngestPage = () => {
  const [activeTab, setActiveTab] = useState<"csv" | "single" | "batch">("csv");

  const [apiKey, setApiKey] = useState("");

  const [file, setFile] = useState<File | null>(null);

  const [status, setStatus] = useState<"success" | "error" | null>(null);

  const [message, setMessage] = useState("");

  const [eventName, setEventName] = useState("purchase");

  const [properties, setProperties] = useState(`{
  "amount": 99,
  "currency": "USD"
}`);

  const [batchEvents, setBatchEvents] = useState(`[
  {
    "event_name": "signup",
    "timestamp": "2026-06-06T10:00:00Z",
    "properties": {
      "plan": "pro"
    }
  },
  {
    "event_name": "purchase",
    "timestamp": "2026-06-06T10:05:00Z",
    "properties": {
      "amount": 149
    }
  }
]`);

  const [loading, setLoading] = useState(false);

  const [responseLog, setResponseLog] = useState("");

  const canIngest = isOwner() || isAdmin();

  // CSV UPLOAD

  const uploadCSV = async () => {
    if (!file) {
      alert("Please select a CSV file");

      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("file", file);

      const response = await api.post("/uploads/csv", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 200) {
        setStatus("success");

        setMessage("CSV uploaded successfully");
      }
      setResponseLog(JSON.stringify(response.data, null, 2));
    } catch (err: any) {
      setStatus("error");
      setMessage(err?.response?.data?.detail || "CSV upload failed");
      setResponseLog(
        JSON.stringify(
          err?.response?.data || {
            detail: "CSV upload failed",
          },
          null,
          2,
        ),
      );
    } finally {
      setLoading(false);
    }
  };

  // SINGLE EVENT

  const sendSingleEvent = async () => {
    if (!apiKey.trim()) {
      setStatus("error");

      setMessage("API key is required");

      return;
    }
    try {
      setLoading(true);

      const payload = {
        event_name: eventName,

        timestamp: new Date().toISOString(),

        properties: JSON.parse(properties),
      };

      const response = await api.post("/events", payload, {
        headers: {
          "X-API-KEY": apiKey,
        },
      });
      if (response.status === 200) {
        setStatus("success");

        setMessage("Event queued successfully");
      }
      setResponseLog(JSON.stringify(response.data, null, 2));
    } catch (err: any) {
      setStatus("error");
      setMessage(err?.response?.data?.detail || "Failed to send event");

      setResponseLog(
        JSON.stringify(
          err?.response?.data || {
            detail: "Failed to send event",
          },
          null,
          2,
        ),
      );
    } finally {
      setLoading(false);
    }
  };

  // BATCH EVENTS

  const sendBatchEvents = async () => {
    if (!apiKey.trim()) {
      setStatus("error");

      setMessage("API key is required");

      return;
    }
    try {
      setLoading(true);

      const parsedBatch = JSON.parse(batchEvents);

      const response = await api.post(
        "/events/batch",
        {
          events: parsedBatch,
        },
        {
          headers: {
            "X-API-KEY": apiKey,
          },
        },
      );

      if (response.status === 200) {
        setStatus("success");

        setMessage("Event queued successfully");
      }

      setResponseLog(JSON.stringify(response.data, null, 2));
    } catch (err: any) {
      setStatus("error");
      setMessage(err?.response?.data?.detail || "Failed to send batch");

      setResponseLog(
        JSON.stringify(
          err?.response?.data || {
            detail: "Failed to send batch",
          },
          null,
          2,
        ),
      );
    } finally {
      setLoading(false);
    }
  };

  // CURL PREVIEW

  const curlPreview = useMemo(() => {
    const endpoint = activeTab === "single" ? "/events" : "/events/batch";

    const payload =
      activeTab === "single"
        ? JSON.stringify(
            {
              event_name: eventName,
              timestamp: new Date().toISOString(),
              properties: JSON.parse(properties),
            },
            null,
            2,
          )
        : {
            events: JSON.parse(batchEvents),
          };

    return `curl -X POST http://localhost:8000${endpoint} \\
-H "Content-Type: application/json" \\
-H "X-API-KEY: ${apiKey || "YOUR_API_KEY"}" \\
-d '${payload}'`;
  }, [activeTab, apiKey, eventName, properties, batchEvents]);

  const copyCurl = async () => {
    await navigator.clipboard.writeText(curlPreview);

    alert("cURL copied");
  };

  if (!canIngest) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-8">
        <div className="bg-white border rounded-2xl shadow-sm p-10 max-w-lg text-center">
          <h1 className="text-3xl font-bold mb-4">Access Restricted</h1>

          <p className="text-gray-600">
            You do not have permission to access the ingestion console.
          </p>
        </div>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <Navbar />
      <div className="max-w-7xl mx-auto">
        {/* HEADER */}

        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Ingestion Console</h1>

          <p className="text-gray-600">
            Upload analytics data or simulate ingestion pipelines.
          </p>
        </div>

        {/* API KEY */}

        {(activeTab === "single" || activeTab === "batch") && (
          <div className="bg-white border rounded-2xl p-6 mb-8 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Database size={22} />

              <h2 className="text-xl font-semibold">API Authentication</h2>
            </div>

            <input
              type="text"
              placeholder="Paste API Key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full border rounded-xl p-4"
            />
          </div>
        )}

        {/* TABS */}

        <div className="flex gap-4 mb-8 flex-wrap">
          <button
            onClick={() => setActiveTab("csv")}
            className={`px-5 py-3 rounded-xl font-medium transition ${
              activeTab === "csv" ? "bg-black text-white" : "bg-white border"
            }`}
          >
            CSV Upload
          </button>

          <button
            onClick={() => setActiveTab("single")}
            className={`px-5 py-3 rounded-xl font-medium transition ${
              activeTab === "single" ? "bg-black text-white" : "bg-white border"
            }`}
          >
            Single Event
          </button>

          <button
            onClick={() => setActiveTab("batch")}
            className={`px-5 py-3 rounded-xl font-medium transition ${
              activeTab === "batch" ? "bg-black text-white" : "bg-white border"
            }`}
          >
            Batch Events
          </button>
        </div>
        {message && (
          <div
            className={`mb-8 p-4 rounded-xl border ${
              status === "success"
                ? "bg-green-50 border-green-200 text-green-700"
                : "bg-red-50 border-red-200 text-red-700"
            }`}
          >
            {message}
          </div>
        )}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* LEFT PANEL */}

          <div className="bg-white rounded-2xl border shadow-sm p-6">
            {/* CSV */}

            {activeTab === "csv" && (
              <>
                <div className="flex items-center gap-3 mb-6">
                  <Upload size={22} />

                  <h2 className="text-xl font-semibold">CSV Upload</h2>
                </div>

                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="w-full border rounded-xl p-4"
                />

                <button
                  onClick={uploadCSV}
                  disabled={loading}
                  className="mt-5 w-full bg-black text-white py-4 rounded-xl flex items-center justify-center gap-2"
                >
                  <Upload size={18} />

                  {loading ? "Uploading..." : "Upload CSV"}
                </button>
              </>
            )}

            {/* SINGLE */}

            {activeTab === "single" && (
              <>
                <h2 className="text-xl font-semibold mb-6">
                  Single Event Builder
                </h2>

                <input
                  type="text"
                  value={eventName}
                  onChange={(e) => setEventName(e.target.value)}
                  className="w-full border rounded-xl p-4 mb-5"
                />

                <textarea
                  value={properties}
                  onChange={(e) => setProperties(e.target.value)}
                  rows={14}
                  className="w-full border rounded-xl p-4 font-mono text-sm"
                />

                <button
                  onClick={sendSingleEvent}
                  disabled={loading}
                  className="mt-5 w-full bg-black text-white py-4 rounded-xl flex items-center justify-center gap-2"
                >
                  <Send size={18} />

                  {loading ? "Sending..." : "Send Event"}
                </button>
              </>
            )}

            {/* BATCH */}

            {activeTab === "batch" && (
              <>
                <h2 className="text-xl font-semibold mb-6">
                  Batch Event Builder
                </h2>

                <textarea
                  value={batchEvents}
                  onChange={(e) => setBatchEvents(e.target.value)}
                  rows={18}
                  className="w-full border rounded-xl p-4 font-mono text-sm"
                />

                <button
                  onClick={sendBatchEvents}
                  disabled={loading}
                  className="mt-5 w-full bg-black text-white py-4 rounded-xl flex items-center justify-center gap-2"
                >
                  <Send size={18} />

                  {loading ? "Sending..." : "Send Batch"}
                </button>
              </>
            )}
          </div>

          {/* RIGHT PANEL */}

          <div className="space-y-8">
            {/* CURL */}

            {(activeTab === "single" || activeTab === "batch") && (
              <div className="bg-white rounded-2xl border shadow-sm p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold">cURL Preview</h2>

                  <button
                    onClick={copyCurl}
                    className="flex items-center gap-2 border px-4 py-2 rounded-lg hover:bg-gray-100"
                  >
                    <Copy size={16} />
                    Copy
                  </button>
                </div>

                <pre className="bg-gray-100 p-4 rounded-xl overflow-auto text-sm whitespace-pre-wrap">
                  {curlPreview}
                </pre>
              </div>
            )}

            {/* RESPONSE */}

            <div className="bg-white rounded-2xl border shadow-sm p-6">
              <h2 className="text-xl font-semibold mb-4">Response Console</h2>

              <pre className="bg-gray-100 p-4 rounded-xl overflow-auto text-sm min-h-[250px] whitespace-pre-wrap">
                {responseLog || "No requests yet"}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IngestPage;
