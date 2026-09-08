/**
 * Type definitions for EVM Project Management
 */

export interface EVMIndicators {
  bac: number | string;
  pv: string | null;
  ev: string | null;
  ac: number | string;
  cv: string | null;
  sv: string | null;
  cpi: string | null;
  spi: string | null;
  eac: string | null;
  vac: string | null;
}

export interface Activity {
  id: number;
  project_id: number;
  name: string;
  bac: number;
  planned_percentage: number;
  actual_percentage: number;
  actual_cost: number;
  created_at: string;
  updated_at: string;
  indicators: EVMIndicators;
}

export interface Project {
  id: number;
  name: string;
  created_at: string;
  activities: Activity[];
  indicators: EVMIndicators;
}

export interface ActivityFormData {
  name: string;
  bac: number;
  planned_percentage: number;
  actual_percentage: number;
  actual_cost: number;
}
