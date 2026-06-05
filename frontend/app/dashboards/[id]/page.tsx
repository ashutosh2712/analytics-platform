"use client";

import { useEffect, useState } from "react";

import { useParams } from "next/navigation";

import api from "@/lib/api";

import WidgetCard from "@/components/WidgetCard";

import Navbar from "@/components/Navbar";

import ProtectedRoute from "@/components/ProtectedRoute";

import Link from "next/link";

const DashboardDetailPage = () => {
  const params = useParams();

  const dashboardId = params.id;

  const [dashboardData, setDashboardData] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  const [title, setTitle] = useState("");

  const [metric, setMetric] = useState("count");

  const [chartType, setChartType] = useState("card");

  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (dashboardId) {
      fetchDashboardData();
    }
  }, [dashboardId]);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get(`/dashboards/${dashboardId}/data`);

      setDashboardData(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const createWidget = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setCreating(true);

      await api.post("/widgets", {
        dashboard_id: Number(dashboardId),

        title,

        metric,

        chart_type: chartType,
      });

      setTitle("");

      fetchDashboardData();
    } catch (error) {
      console.error(error);
    } finally {
      setCreating(false);
    }
  };

  if (loading) {
    return <div className="p-8">Loading dashboard...</div>;
  }

  return (
    <ProtectedRoute>
      {" "}
      <div className="min-h-screen bg-gray-100 p-8">
        <Navbar />
        <Link href="/dashboards" className="text-blue-600 mb-4 inline-block">
          ← Back to Dashboards
        </Link>
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">{dashboardData.dashboard_name}</h1>
        </div>

        <form
          onSubmit={createWidget}
          className="bg-white rounded-xl shadow-md p-6 mb-8 grid grid-cols-1 md:grid-cols-4 gap-4"
        >
          <input
            type="text"
            placeholder="Widget Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="border rounded-lg p-3"
          />

          <select
            value={metric}
            onChange={(e) => setMetric(e.target.value)}
            className="border rounded-lg p-3"
          >
            <option value="count">Total Count</option>

            <option value="timeseries">Timeseries</option>

            <option value="by_name">Events By Name</option>
          </select>

          <select
            value={chartType}
            onChange={(e) => setChartType(e.target.value)}
            className="border rounded-lg p-3"
          >
            <option value="card">Card</option>

            <option value="line">Line Chart</option>

            <option value="bar">Bar Chart</option>
          </select>

          <button
            type="submit"
            disabled={creating}
            className="bg-black text-white rounded-lg px-6"
          >
            {creating ? "Creating..." : "Create Widget"}
          </button>
        </form>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {dashboardData.widgets.map((widget: any) => (
            <WidgetCard
              key={widget.id}
              widget={widget}
              onDelete={fetchDashboardData}
            />
          ))}
        </div>
      </div>{" "}
    </ProtectedRoute>
  );
};

export default DashboardDetailPage;
