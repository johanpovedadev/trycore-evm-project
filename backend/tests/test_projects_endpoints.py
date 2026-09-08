"""Integration tests for project endpoints."""



class TestProjectEndpoints:
    """Test project CRUD endpoints."""

    def test_create_project_success(self, client):
        """Test creating a project."""
        payload = {"name": "Test Project"}
        response = client.post("/projects", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Project"
        assert "id" in data
        assert "created_at" in data
        assert "activities" in data
        assert data["activities"] == []

    def test_list_projects_empty(self, client):
        """Test listing projects when empty."""
        response = client.get("/projects")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_and_list_projects(self, client):
        """Test creating multiple projects and listing them."""
        client.post("/projects", json={"name": "Project 1"})
        client.post("/projects", json={"name": "Project 2"})

        response = client.get("/projects")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_get_project_not_found(self, client):
        """Test getting non-existent project."""
        response = client.get("/projects/9999")

        assert response.status_code == 404

    def test_get_project_success(self, client):
        """Test getting a project."""
        create_response = client.post("/projects", json={"name": "Test Project"})
        project_id = create_response.json()["id"]

        response = client.get(f"/projects/{project_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert data["name"] == "Test Project"
        assert "indicators" in data

    def test_update_project_success(self, client):
        """Test updating a project."""
        create_response = client.post("/projects", json={"name": "Original Name"})
        project_id = create_response.json()["id"]

        response = client.put(f"/projects/{project_id}", json={"name": "Updated Name"})

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_update_project_not_found(self, client):
        """Test updating non-existent project."""
        response = client.put("/projects/9999", json={"name": "New Name"})

        assert response.status_code == 404

    def test_delete_project_success(self, client):
        """Test deleting a project."""
        create_response = client.post("/projects", json={"name": "To Delete"})
        project_id = create_response.json()["id"]

        response = client.delete(f"/projects/{project_id}")

        assert response.status_code == 204

        get_response = client.get(f"/projects/{project_id}")
        assert get_response.status_code == 404

    def test_delete_project_not_found(self, client):
        """Test deleting non-existent project."""
        response = client.delete("/projects/9999")

        assert response.status_code == 404
