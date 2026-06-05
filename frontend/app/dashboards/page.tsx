"use client";

import { useEffect, useState } from "react";

import api from "@/lib/api";

import Navbar from "@/components/Navbar";

import ProtectedRoute from "@/components/ProtectedRoute";

const DashboardsPage = () => {
  const [dashboards, setDashboards] = useState<any[]>([]);

  const [name, setName] = useState("");

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDashboards();
  }, []);

  const fetchDashboards = async () => {
    try {
      const response = await api.get("/dashboards");

      setDashboards(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const createDashboard = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setLoading(true);

      await api.post("/dashboards", {
        name,
      });

      setName("");

      fetchDashboards();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="p-8 min-h-screen bg-gray-100">
        <Navbar />
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

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {dashboards.map((dashboard) => (
            <a
              key={dashboard.id}
              href={`/dashboards/${dashboard.id}`}
              className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition"
            >
              <h2 className="text-xl font-semibold mb-2">{dashboard.name}</h2>

              <p className="text-gray-500">Open Dashboard →</p>
            </a>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardsPage;
