import type { EVMIndicators } from '../types';

interface IndicatorsPanelProps {
  indicators: EVMIndicators;
  title?: string;
}

function getHealthStatus(value: string | number | null): 'good' | 'warning' | 'danger' | 'neutral' {
  if (value === null) return 'neutral';

  const num = typeof value === 'string' ? parseFloat(value) : value;

  if (isNaN(num)) return 'neutral';
  if (num > 1.1) return 'good';
  if (num >= 0.9) return 'warning';
  return 'danger';
}

function getSPIStatus(value: string | number | null): 'good' | 'warning' | 'danger' | 'neutral' {
  if (value === null) return 'neutral';

  const num = typeof value === 'string' ? parseFloat(value) : value;

  if (isNaN(num)) return 'neutral';
  if (num > 1.05) return 'good';
  if (num >= 0.95) return 'warning';
  return 'danger';
}

function getHealthLabel(status: 'good' | 'warning' | 'danger' | 'neutral'): string {
  switch (status) {
    case 'good':
      return 'Good';
    case 'warning':
      return 'At Risk';
    case 'danger':
      return 'Over Budget';
    case 'neutral':
      return 'N/A';
  }
}

function getSPILabel(status: 'good' | 'warning' | 'danger' | 'neutral'): string {
  switch (status) {
    case 'good':
      return 'Ahead of Schedule';
    case 'warning':
      return 'On Schedule';
    case 'danger':
      return 'Behind Schedule';
    case 'neutral':
      return 'N/A';
  }
}

interface IndicatorRowProps {
  label: string;
  value: string | number | null;
  unit?: string;
  showHealth?: boolean;
  isSPI?: boolean;
}

function IndicatorRow({ label, value, unit = '', showHealth = false, isSPI = false }: IndicatorRowProps) {
  if (value === null) {
    return (
      <div className="indicator-row">
        <div className="indicator-label">{label}</div>
        <div className="indicator-value">N/A</div>
      </div>
    );
  }

  const status = showHealth ? (isSPI ? getSPIStatus(value) : getHealthStatus(value)) : 'neutral';
  const label_text = isSPI ? getSPILabel(status) : getHealthLabel(status);

  return (
    <div className="indicator-row">
      <div className="indicator-label">{label}</div>
      <div className={`indicator-value status-${status}`}>
        {value}
        {unit && <span className="unit">{unit}</span>}
      </div>
      {showHealth && (
        <div className={`health-badge badge-${status}`}>
          {label_text}
        </div>
      )}
    </div>
  );
}

export function IndicatorsPanel({ indicators, title = 'Consolidated Indicators' }: IndicatorsPanelProps) {
  return (
    <div className="indicators-panel">
      <h3>{title}</h3>

      <div className="indicators-grid">
        <div className="indicator-group">
          <h4>Budget & Costs</h4>
          <IndicatorRow label="Budget at Completion" value={indicators.bac} />
          <IndicatorRow label="Planned Value" value={indicators.pv} />
          <IndicatorRow label="Earned Value" value={indicators.ev} />
          <IndicatorRow label="Actual Cost" value={indicators.ac} />
        </div>

        <div className="indicator-group">
          <h4>Variances</h4>
          <IndicatorRow
            label="Cost Variance"
            value={indicators.cv}
            showHealth={false}
          />
          <IndicatorRow
            label="Schedule Variance"
            value={indicators.sv}
            showHealth={false}
          />
        </div>

        <div className="indicator-group">
          <h4>Performance Indices</h4>
          <IndicatorRow
            label="Cost Performance Index"
            value={indicators.cpi}
            showHealth={true}
          />
          <IndicatorRow
            label="Schedule Performance Index"
            value={indicators.spi}
            showHealth={true}
            isSPI={true}
          />
        </div>

        <div className="indicator-group">
          <h4>Forecasts</h4>
          <IndicatorRow label="Estimate at Completion" value={indicators.eac} />
          <IndicatorRow label="Variance at Completion" value={indicators.vac} />
        </div>
      </div>
    </div>
  );
}
