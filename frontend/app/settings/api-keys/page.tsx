"use client";

import { useEffect, useState } from "react";

import api from "@/lib/api";

import Navbar from "@/components/Navbar";

import ProtectedRoute from "@/components/ProtectedRoute";

const APIKeysPage = () => {
  const [keys, setKeys] = useState<any[]>([]);

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [error, setError] = useState("");

  const [keyName, setKeyName] = useState("");

  useEffect(() => {
    fetchKeys();
  }, []);

  const fetchKeys = async () => {
    try {
      const response = await api.get("/api-keys");

      console.log(response.data);

      setKeys(response.data.api_keys || response.data);
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to load API keys");
    }
  };

  const createKey = async () => {
    if (!keyName.trim()) {
      setError("Please enter API key name");

      return;
    }

    try {
      setLoading(true);

      setError("");

      setMessage("");

      const response = await api.post("/api-keys", {
        name: keyName,
      });

      setMessage(
        `New API Key:
${response.data.key}`,
      );

      setKeyName("");

      fetchKeys();
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to create API key");
    } finally {
      setLoading(false);
    }
  };

  const revokeKey = async (id: number) => {
    try {
      setError("");

      await api.post(`/api-keys/${id}/revoke`);

      setMessage("API key revoked successfully");

      fetchKeys();
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to revoke key");
    }
  };

  const rotateKey = async (id: number) => {
    try {
      setError("");

      const response = await api.post(`/api-keys/${id}/rotate`);

      setMessage(`Rotated Key:${response.data.key}`);

      fetchKeys();
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to rotate key");
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <Navbar />

        <div className="max-w-5xl mx-auto p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">API Key Management</h1>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6 mb-8 flex gap-4">
            <input
              type="text"
              placeholder="API Key Name"
              value={keyName}
              onChange={(e) => setKeyName(e.target.value)}
              className="flex-1 border rounded-lg px-4 py-3"
            />

            <button
              onClick={createKey}
              disabled={loading}
              className="bg-black text-white px-6 py-3 rounded-lg"
            >
              {loading ? "Creating..." : "Create API Key"}
            </button>
          </div>

          {message && (
            <div className="bg-green-100 border border-green-300 text-green-800 p-4 rounded-lg mb-6 break-all">
              {message}
            </div>
          )}

          {error && (
            <div className="bg-red-100 border border-red-300 text-red-800 p-4 rounded-lg mb-6">
              {error}
            </div>
          )}

          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-200">
                <tr>
                  <th className="text-left p-4">ID</th>

                  <th className="text-left p-4">Name</th>

                  <th className="text-left p-4">Status</th>

                  <th className="text-left p-4">Actions</th>
                </tr>
              </thead>

              <tbody>
                {Array.isArray(keys) &&
                  keys.map((key) => (
                    <tr key={key.id} className="border-t">
                      <td className="p-4">{key.id}</td>

                      <td className="p-4">{key.name}</td>

                      <td className="p-4">
                        {key.is_active ? (
                          <span className="text-green-600">Active</span>
                        ) : (
                          <span className="text-red-600">Revoked</span>
                        )}
                      </td>

                      <td className="p-4 flex gap-2">
                        <button
                          onClick={() => rotateKey(key.id)}
                          className="bg-blue-600 text-white px-4 py-2 rounded-lg"
                        >
                          Rotate
                        </button>

                        <button
                          onClick={() => revokeKey(key.id)}
                          className="bg-red-600 text-white px-4 py-2 rounded-lg"
                        >
                          Revoke
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default APIKeysPage;
