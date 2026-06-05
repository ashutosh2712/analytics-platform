"use client";

import { useRef, useState } from "react";

import api from "@/lib/api";

import Navbar from "@/components/Navbar";

import ProtectedRoute from "@/components/ProtectedRoute";

const IngestPage = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [error, setError] = useState("");

  const handleFileSelect = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");

      return;
    }

    try {
      setLoading(true);

      setError("");

      setMessage("");

      const formData = new FormData();

      formData.append("file", file);

      const response = await api.post("/uploads/csv", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage(
        `${response.data.message}
           (${response.data.total_rows} rows)`,
      );
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <Navbar />

        <div className="max-w-2xl mx-auto p-8">
          <div className="bg-white rounded-xl shadow-md p-8">
            <h1 className="text-3xl font-bold mb-6">CSV Event Upload</h1>

            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
            />

            <button
              onClick={handleFileSelect}
              className="bg-gray-200 px-6 py-3 rounded-lg mr-4"
            >
              Select CSV File
            </button>

            <button
              onClick={handleUpload}
              disabled={loading}
              className="bg-black text-white px-6 py-3 rounded-lg"
            >
              {loading ? "Uploading..." : "Upload CSV"}
            </button>

            {file && (
              <p className="mt-4 text-sm text-gray-600">
                Selected: {file.name}
              </p>
            )}

            {message && <p className="mt-6 text-green-600">{message}</p>}

            {error && <p className="mt-6 text-red-600">{error}</p>}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default IngestPage;
