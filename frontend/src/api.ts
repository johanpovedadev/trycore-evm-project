/**
 * API service for backend communication
 */

import type { Project, Activity, ActivityFormData } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    if (response.status === 204) {
      return null as unknown as T;
    }

    return response.json() as Promise<T>;
  }

  // Projects
  async getProjects(): Promise<Project[]> {
    return this.request<Project[]>('/projects');
  }

  async getProject(id: number): Promise<Project> {
    return this.request<Project>(`/projects/${id}`);
  }

  async createProject(name: string): Promise<Project> {
    return this.request<Project>('/projects', {
      method: 'POST',
      body: JSON.stringify({ name }),
    });
  }

  async updateProject(id: number, name: string): Promise<Project> {
    return this.request<Project>(`/projects/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ name }),
    });
  }

  async deleteProject(id: number): Promise<void> {
    await this.request(`/projects/${id}`, { method: 'DELETE' });
  }

  // Activities
  async getActivities(projectId: number): Promise<Activity[]> {
    return this.request<Activity[]>(`/projects/${projectId}/activities`);
  }

  async getActivity(id: number): Promise<Activity> {
    return this.request<Activity>(`/activities/${id}`);
  }

  async createActivity(
    projectId: number,
    data: ActivityFormData
  ): Promise<Activity> {
    return this.request<Activity>(`/projects/${projectId}/activities`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateActivity(id: number, data: Partial<ActivityFormData>): Promise<Activity> {
    return this.request<Activity>(`/activities/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteActivity(id: number): Promise<void> {
    await this.request(`/activities/${id}`, { method: 'DELETE' });
  }
}

export const api = new ApiClient(API_BASE_URL);
