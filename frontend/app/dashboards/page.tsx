"use client";

import { useEffect, useState } from "react";

import api from "@/lib/api";

const DashboardsPage = () => {
  const [dashboards, setDashboards] = useState<any[]>([]);

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

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboards</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {dashboards.map((dashboard) => (
          <a
            key={dashboard.id}
            href={`/dashboards/${dashboard.id}`}
            className="border rounded-lg p-6 hover:shadow-lg transition"
          >
            <h2 className="text-xl font-semibold">{dashboard.name}</h2>
          </a>
        ))}
      </div>
    </div>
  );
};

export default DashboardsPage;
