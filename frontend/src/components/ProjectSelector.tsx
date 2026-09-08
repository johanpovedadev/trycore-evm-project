import { useState, useEffect } from 'react';
import type { Project } from '../types';
import { api } from '../api';

interface ProjectSelectorProps {
  onProjectSelect: (project: Project) => void;
  selectedProjectId?: number;
}

export function ProjectSelector({ onProjectSelect, selectedProjectId }: ProjectSelectorProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newProjectName, setNewProjectName] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  async function loadProjects() {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getProjects();
      setProjects(data);
      if (data.length > 0 && !selectedProjectId) {
        onProjectSelect(data[0]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load projects');
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateProject(e: React.FormEvent) {
    e.preventDefault();
    if (!newProjectName.trim()) return;

    try {
      setCreating(true);
      setError(null);
      const newProject = await api.createProject(newProjectName);
      setProjects([...projects, newProject]);
      setNewProjectName('');
      onProjectSelect(newProject);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
    } finally {
      setCreating(false);
    }
  }

  if (loading) return <div className="project-selector-container">Loading projects...</div>;

  return (
    <div className="project-selector-container">
      <div className="project-form">
        <h3>Create New Project</h3>
        <form onSubmit={handleCreateProject}>
          <input
            type="text"
            placeholder="Project name..."
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            disabled={creating}
          />
          <button type="submit" disabled={creating || !newProjectName.trim()}>
            {creating ? 'Creating...' : 'Create'}
          </button>
        </form>
      </div>

      <div className="projects-list">
        <h3>Projects</h3>
        {error && <div className="error-message">{error}</div>}
        {projects.length === 0 ? (
          <p className="empty-message">No projects yet. Create one above!</p>
        ) : (
          <div className="project-items">
            {projects.map((project) => (
              <div
                key={project.id}
                className={`project-item ${selectedProjectId === project.id ? 'active' : ''}`}
                onClick={() => onProjectSelect(project)}
              >
                <div className="project-name">{project.name}</div>
                <div className="project-activities">
                  {project.activities.length} activities
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
