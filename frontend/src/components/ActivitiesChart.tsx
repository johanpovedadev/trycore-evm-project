import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';
import type { Activity } from '../types';

interface ActivitiesChartProps {
  activities: Activity[];
}

export function ActivitiesChart({ activities }: ActivitiesChartProps) {
  const chartData = activities.map((activity) => ({
    name: activity.name.slice(0, 10),
    fullName: activity.name,
    pv: activity.indicators.pv ? parseFloat(activity.indicators.pv) : 0,
    ev: activity.indicators.ev ? parseFloat(activity.indicators.ev) : 0,
    ac: activity.actual_cost,
  }));

  if (activities.length === 0) {
    return (
      <div className="chart-container">
        <p className="empty-message">No activities to display in chart</p>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <div className="chart-section">
        <h4>PV, EV, AC by Activity</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip
              content={({ payload }) => {
                if (payload && payload.length > 0) {
                  const data = payload[0].payload;
                  return (
                    <div className="tooltip">
                      <p className="tooltip-title">{data.fullName}</p>
                      {payload.map((entry, i) => (
                        <p key={i} style={{ color: entry.color }}>
                          {entry.name}: {entry.value}
                        </p>
                      ))}
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend />
            <Bar dataKey="pv" fill="#3b82f6" name="Planned Value (PV)" />
            <Bar dataKey="ev" fill="#10b981" name="Earned Value (EV)" />
            <Bar dataKey="ac" fill="#ef4444" name="Actual Cost (AC)" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h4>Cumulative Progress</h4>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip
              content={({ payload }) => {
                if (payload && payload.length > 0) {
                  const data = payload[0].payload;
                  return (
                    <div className="tooltip">
                      <p className="tooltip-title">{data.fullName}</p>
                      {payload.map((entry, i) => (
                        <p key={i} style={{ color: entry.color }}>
                          {entry.name}: {entry.value}
                        </p>
                      ))}
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend />
            <Line type="monotone" dataKey="pv" stroke="#3b82f6" name="Planned Value" />
            <Line type="monotone" dataKey="ev" stroke="#10b981" name="Earned Value" />
            <Line type="monotone" dataKey="ac" stroke="#ef4444" name="Actual Cost" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
