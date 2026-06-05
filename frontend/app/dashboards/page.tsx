"use client";

import { useEffect, useState } from "react";

import api from "@/lib/api";

import Navbar from "@/components/Navbar";

import ProtectedRoute from "@/components/ProtectedRoute";
import Link from "next/dist/client/link";

const DashboardsPage = () => {
  const [dashboards, setDashboards] = useState<any[]>([]);

  const [name, setName] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchDashboards();
  }, []);

  const fetchDashboards = async () => {
    try {
      const response = await api.get("/dashboards");

      setDashboards(response.data);
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to load dashboards");
    }
  };

  const createDashboard = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name.trim()) {
      setError("Dashboard name required");

      return;
    }

    try {
      setLoading(true);

      setError("");

      setMessage("");

      await api.post("/dashboards", {
        name,
      });

      setName("");

      setMessage("Dashboard created successfully");

      fetchDashboards();
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to create dashboard");
    } finally {
      setLoading(false);
    }
  };

  const deleteDashboard = async (id: number) => {
    const confirmed = window.confirm("Delete this dashboard?");

    if (!confirmed) {
      return;
    }

    try {
      setError("");

      setMessage("");

      await api.delete(`/dashboards/${id}`);

      setMessage("Dashboard deleted successfully");

      fetchDashboards();
    } catch (err: any) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to delete dashboard");
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <Navbar />

        <div className="p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">Dashboards</h1>
          </div>

          <form
            onSubmit={createDashboard}
            className="bg-white p-6 rounded-xl shadow-md mb-8 flex gap-4"
          >
            <input
              type="text"
              placeholder="Dashboard Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="flex-1 border rounded-lg p-3"
            />

            <button
              type="submit"
              disabled={loading}
              className="bg-black text-white px-6 rounded-lg"
            >
              {loading ? "Creating..." : "Create"}
            </button>
          </form>

          {message && (
            <div className="bg-green-100 border border-green-300 text-green-800 p-4 rounded-lg mb-6">
              {message}
            </div>
          )}

          {error && (
            <div className="bg-red-100 border border-red-300 text-red-800 p-4 rounded-lg mb-6">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Array.isArray(dashboards) &&
              dashboards.map((dashboard) => (
                <div
                  key={dashboard.id}
                  className="bg-white rounded-xl shadow-md p-6"
                >
                  <Link href={`/dashboards/${dashboard.id}`}>
                    <h2 className="text-xl font-semibold mb-4 hover:underline">
                      {dashboard.name}
                    </h2>
                  </Link>

                  <button
                    onClick={() => deleteDashboard(dashboard.id)}
                    className="bg-red-600 text-white px-4 py-2 rounded-lg"
                  >
                    Delete
                  </button>
                </div>
              ))}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardsPage;
