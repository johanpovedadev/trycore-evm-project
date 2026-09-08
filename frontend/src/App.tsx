import { useState } from 'react';
import type { Project } from './types';
import { api } from './api';
import { ProjectSelector } from './components/ProjectSelector';
import { ActivityTable } from './components/ActivityTable';
import { IndicatorsPanel } from './components/IndicatorsPanel';
import { ActivitiesChart } from './components/ActivitiesChart';
import { ActivityForm } from './components/ActivityForm';
import './App.css';

function App() {
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [showActivityForm, setShowActivityForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function reloadProject() {
    if (!selectedProject) return;

    try {
      setLoading(true);
      setError(null);
      const freshProject = await api.getProject(selectedProject.id);
      setSelectedProject(freshProject);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reload project');
    } finally {
      setLoading(false);
    }
  }

  function handleProjectSelect(project: Project) {
    setSelectedProject(project);
    setShowActivityForm(false);
    setError(null);
  }

  async function handleActivitySaved() {
    setShowActivityForm(false);
    await reloadProject();
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Trycore EVM Dashboard</h1>
        <p className="subtitle">Earned Value Management Project Tracking</p>
      </header>

      <div className="app-layout">
        <aside className="sidebar">
          <ProjectSelector
            onProjectSelect={handleProjectSelect}
            selectedProjectId={selectedProject?.id}
          />
        </aside>

        <main className="main-content">
          {selectedProject ? (
            <>
              <div className="project-header">
                <div>
                  <h2>{selectedProject.name}</h2>
                  <p className="project-info">
                    {selectedProject.activities.length} activities
                  </p>
                </div>
                <button
                  className="btn-primary"
                  onClick={() => setShowActivityForm(!showActivityForm)}
                >
                  {showActivityForm ? 'Cancel' : 'Add Activity'}
                </button>
              </div>

              {error && <div className="error-banner">{error}</div>}
              {loading && <div className="loading-banner">Updating...</div>}

              {showActivityForm && (
                <div className="form-section">
                  <h3>New Activity</h3>
                  <ActivityForm
                    projectId={selectedProject.id}
                    onSave={handleActivitySaved}
                    onCancel={() => setShowActivityForm(false)}
                  />
                </div>
              )}

              <div className="dashboard-grid">
                <section className="section-full">
                  <IndicatorsPanel
                    indicators={selectedProject.indicators}
                    title={`${selectedProject.name} - Consolidated Indicators`}
                  />
                </section>

                <section className="section-full">
                  <ActivityTable
                    activities={selectedProject.activities}
                    projectId={selectedProject.id}
                    onActivityUpdated={reloadProject}
                  />
                </section>

                <section className="section-full">
                  <ActivitiesChart activities={selectedProject.activities} />
                </section>
              </div>
            </>
          ) : (
            <div className="empty-state">
              <h2>Welcome to Trycore EVM</h2>
              <p>Select or create a project to get started</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
