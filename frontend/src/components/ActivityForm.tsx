import { useState, useEffect } from 'react';
import type { Activity, ActivityFormData } from '../types';
import { api } from '../api';

interface ActivityFormProps {
  projectId: number;
  activity?: Activity;
  onSave: () => void;
  onCancel: () => void;
}

export function ActivityForm({ projectId, activity, onSave, onCancel }: ActivityFormProps) {
  const [formData, setFormData] = useState<ActivityFormData>({
    name: '',
    bac: 0,
    planned_percentage: 0,
    actual_percentage: 0,
    actual_cost: 0,
  });
  const [bacText, setBacText] = useState('');
  const [plannedPercentageText, setPlannedPercentageText] = useState('');
  const [actualPercentageText, setActualPercentageText] = useState('');
  const [actualCostText, setActualCostText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (activity) {
      setFormData({
        name: activity.name,
        bac: activity.bac,
        planned_percentage: activity.planned_percentage,
        actual_percentage: activity.actual_percentage,
        actual_cost: activity.actual_cost,
      });
      setBacText(String(activity.bac));
      setPlannedPercentageText(String(activity.planned_percentage));
      setActualPercentageText(String(activity.actual_percentage));
      setActualCostText(String(activity.actual_cost));
    }
  }, [activity]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!formData.name.trim()) {
      setError('Activity name is required');
      return;
    }

    const bac = bacText === '' ? 0 : parseFloat(bacText);
    const planned = plannedPercentageText === '' ? 0 : parseFloat(plannedPercentageText);
    const actual = actualPercentageText === '' ? 0 : parseFloat(actualPercentageText);
    const ac = actualCostText === '' ? 0 : parseFloat(actualCostText);

    if (isNaN(bac) || bac <= 0) {
      setError('Budget at Completion (BAC) is required and must be greater than 0');
      return;
    }

    if (isNaN(planned) || planned < 0 || planned > 100) {
      setError('Planned Progress must be between 0 and 100');
      return;
    }

    if (isNaN(actual) || actual < 0 || actual > 100) {
      setError('Actual Progress must be between 0 and 100');
      return;
    }

    if (isNaN(ac) || ac < 0) {
      setError('Actual Cost must be 0 or greater');
      return;
    }

    const submitData: ActivityFormData = {
      name: formData.name,
      bac,
      planned_percentage: planned,
      actual_percentage: actual,
      actual_cost: ac,
    };

    try {
      setLoading(true);
      setError(null);

      if (activity) {
        await api.updateActivity(activity.id, submitData);
      } else {
        await api.createActivity(projectId, submitData);
      }
      onSave();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save activity');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="activity-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <div className="form-group">
          <label>Activity Name *</label>
          <input
            type="text"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g., Design, Development, Testing"
            disabled={loading}
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Budget at Completion (BAC) *</label>
          <input
            type="number"
            required
            min="0.01"
            step="0.01"
            value={bacText}
            onChange={(e) => setBacText(e.target.value)}
            placeholder="0.00"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Planned Progress (%)</label>
          <input
            type="number"
            min="0"
            max="100"
            step="0.01"
            value={plannedPercentageText}
            onChange={(e) => setPlannedPercentageText(e.target.value)}
            placeholder="0"
            disabled={loading}
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Actual Progress (%)</label>
          <input
            type="number"
            min="0"
            max="100"
            step="0.01"
            value={actualPercentageText}
            onChange={(e) => setActualPercentageText(e.target.value)}
            placeholder="0"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Actual Cost (AC)</label>
          <input
            type="number"
            min="0"
            step="0.01"
            value={actualCostText}
            onChange={(e) => setActualCostText(e.target.value)}
            placeholder="0.00"
            disabled={loading}
          />
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="form-actions">
        <button type="submit" disabled={loading}>
          {loading ? 'Saving...' : activity ? 'Update' : 'Create'}
        </button>
        <button type="button" onClick={onCancel} disabled={loading}>
          Cancel
        </button>
      </div>
    </form>
  );
}
