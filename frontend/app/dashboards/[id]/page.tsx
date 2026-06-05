"use client";

import { useEffect, useState } from "react";

import { useParams } from "next/navigation";

import api from "@/lib/api";

import WidgetCard from "@/components/WidgetCard";

const DashboardDetailPage = () => {
  const params = useParams();

  const dashboardId = params.id;

  const [dashboardData, setDashboardData] = useState<any>(null);

  const [loading, setLoading] = useState(true);

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

  if (loading) {
    return <div className="p-8">Loading dashboard...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">
        {dashboardData.dashboard_name}
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {dashboardData.widgets.map((widget: any) => (
          <WidgetCard key={widget.id} widget={widget} />
        ))}
      </div>
    </div>
  );
};

export default DashboardDetailPage;
