import { useState } from 'react';
import type { Activity } from '../types';
import { api } from '../api';
import { ActivityForm } from './ActivityForm';

interface ActivityTableProps {
  activities: Activity[];
  projectId: number;
  onActivityUpdated: () => void;
}

export function ActivityTable({
  activities,
  projectId,
  onActivityUpdated,
}: ActivityTableProps) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleDelete(id: number) {
    if (!window.confirm('Are you sure you want to delete this activity?')) return;

    try {
      setDeletingId(id);
      setError(null);
      await api.deleteActivity(id);
      await onActivityUpdated();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete activity');
    } finally {
      setDeletingId(null);
    }
  }

  function getStatusBadge(value: number | string | null) {
    if (value === null) return <span className="badge badge-neutral">N/A</span>;

    const num = typeof value === 'string' ? parseFloat(value) : value;

    if (num > 1.1) return <span className="badge badge-success">Good</span>;
    if (num >= 0.9) return <span className="badge badge-warning">At Risk</span>;
    return <span className="badge badge-danger">Over Budget</span>;
  }

  function getSPIBadge(value: number | string | null) {
    if (value === null) return <span className="badge badge-neutral">N/A</span>;

    const num = typeof value === 'string' ? parseFloat(value) : value;

    if (num > 1.05) return <span className="badge badge-success">Ahead of Schedule</span>;
    if (num >= 0.95) return <span className="badge badge-warning">On Schedule</span>;
    return <span className="badge badge-danger">Behind Schedule</span>;
  }

  return (
    <div className="activity-table-container">
      <h3>Activities</h3>
      {error && <div className="error-message">{error}</div>}

      {activities.length === 0 ? (
        <p className="empty-message">No activities yet. Add one below.</p>
      ) : (
        <div className="table-wrapper">
          <table className="activity-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>BAC</th>
                <th>Planned %</th>
                <th>Actual %</th>
                <th>AC</th>
                <th>PV</th>
                <th>EV</th>
                <th>CV</th>
                <th>SV</th>
                <th>CPI</th>
                <th>SPI</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((activity) => (
                <tr key={activity.id}>
                  <td className="activity-name">
                    {editingId === activity.id ? (
                      <ActivityForm
                        projectId={projectId}
                        activity={activity}
                        onSave={() => {
                          setEditingId(null);
                          onActivityUpdated();
                        }}
                        onCancel={() => setEditingId(null)}
                      />
                    ) : (
                      activity.name
                    )}
                  </td>
                  <td>{activity.bac}</td>
                  <td>{activity.planned_percentage}%</td>
                  <td>{activity.actual_percentage}%</td>
                  <td>{activity.actual_cost}</td>
                  <td className="value-cell">{activity.indicators.pv || 'N/A'}</td>
                  <td className="value-cell">{activity.indicators.ev || 'N/A'}</td>
                  <td className={`value-cell ${activity.indicators.cv && parseFloat(activity.indicators.cv) < 0 ? 'negative' : ''}`}>
                    {activity.indicators.cv || 'N/A'}
                  </td>
                  <td className={`value-cell ${activity.indicators.sv && parseFloat(activity.indicators.sv) < 0 ? 'negative' : ''}`}>
                    {activity.indicators.sv || 'N/A'}
                  </td>
                  <td className="indicator-cell">
                    {activity.indicators.cpi !== null ? (
                      <>
                        <span>{activity.indicators.cpi}</span>
                        {getStatusBadge(activity.indicators.cpi)}
                      </>
                    ) : (
                      'N/A'
                    )}
                  </td>
                  <td className="indicator-cell">
                    {activity.indicators.spi !== null ? (
                      <>
                        <span>{activity.indicators.spi}</span>
                        {getSPIBadge(activity.indicators.spi)}
                      </>
                    ) : (
                      'N/A'
                    )}
                  </td>
                  <td className="actions-cell">
                    {editingId === activity.id ? null : (
                      <>
                        <button
                          className="btn-small btn-edit"
                          onClick={() => setEditingId(activity.id)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn-small btn-delete"
                          onClick={() => handleDelete(activity.id)}
                          disabled={deletingId === activity.id}
                        >
                          {deletingId === activity.id ? 'Deleting...' : 'Delete'}
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
