"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

const WidgetCard = ({ widget }: any) => {
  const renderContent = () => {
    if (widget.metric === "count") {
      return (
        <div className="text-5xl font-bold">{widget.data.total_events}</div>
      );
    }

    if (widget.metric === "timeseries") {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={widget.data}>
            <XAxis dataKey="date" />

            <YAxis />

            <Tooltip />

            <Line type="monotone" dataKey="count" />
          </LineChart>
        </ResponsiveContainer>
      );
    }

    if (widget.metric === "by_name") {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={widget.data}>
            <XAxis dataKey="event_name" />

            <YAxis />

            <Tooltip />

            <Bar dataKey="count" />
          </BarChart>
        </ResponsiveContainer>
      );
    }

    return <div>Unsupported widget</div>;
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-xl font-semibold mb-6">{widget.title}</h2>

      {renderContent()}
    </div>
  );
};

export default WidgetCard;
