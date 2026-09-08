"""Integration tests for activity endpoints."""
from decimal import Decimal


class TestActivityEndpoints:
    """Test activity CRUD endpoints."""

    def test_create_activity_success(self, client):
        """Test creating an activity."""
        project_response = client.post("/projects", json={"name": "Test Project"})
        project_id = project_response.json()["id"]

        activity_payload = {
            "name": "Task 1",
            "bac": 1000,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post(
            f"/projects/{project_id}/activities", json=activity_payload
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Task 1"
        assert data["bac"] == 1000
        assert "indicators" in data
        assert data["indicators"]["cpi"] == "1.13"

    def test_create_activity_invalid_project(self, client):
        """Test creating activity for non-existent project."""
        activity_payload = {
            "name": "Task 1",
            "bac": 1000,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post("/projects/9999/activities", json=activity_payload)

        assert response.status_code == 404

    def test_create_activity_invalid_bac(self, client):
        """Test creating activity with invalid BAC."""
        project_response = client.post("/projects", json={"name": "Test Project"})
        project_id = project_response.json()["id"]

        activity_payload = {
            "name": "Task 1",
            "bac": 0,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post(
            f"/projects/{project_id}/activities", json=activity_payload
        )

        assert response.status_code == 422

    def test_list_activities_for_project(self, client):
        """Test listing activities for a project."""
        project_response = client.post("/projects", json={"name": "Test Project"})
        project_id = project_response.json()["id"]

        client.post(
            f"/projects/{project_id}/activities",
            json={
                "name": "Task 1",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 45,
                "actual_cost": 400,
            },
        )

        response = client.get(f"/projects/{project_id}/activities")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Task 1"

    def test_get_activity_success(self, client):
        """Test getting a single activity."""
        project_response = client.post("/projects", json={"name": "Test Project"})
        project_id = project_response.json()["id"]

        activity_response = client.post(
            f"/projects/{project_id}/activities",
            json={
                "name": "Task 1",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 45,
                "actual_cost": 400,
            },
        )
        activity_id = activity_response.json()["id"]

        response = client.get(f"/activities/{activity_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == activity_id
        assert data["name"] == "Task 1"

    def test_get_activity_not_found(self, client):
        """Test getting non-existent activity."""
        response = client.get("/activities/9999")

        assert response.status_code == 404

    def test_update_activity_success(self, client):
        """Test updating an activity."""
        project_response = client.post("/projects", json={"name": "Test Project"})
        project_id = project_response.json()["id"]

        activity_response = client.post(
            f"/projects/{project_id}/activities",
            json={
                "name": "Task 1",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 45,
                "actual_cost": 400,
            },
        )
        activity_id = activity_response.json()["id"]

        response = client.put(
            f"/activities/{activity_id}",
            json={"name": "Updated Task", "actual_percentage": 60},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Task"
        assert data["actual_percentage"] == 60

    def test_update_activity_not_found(self, client):
        """Test updating non-existent activity."""
        response = client.put(
            "/activities/9999", json={"name": "Updated Task"}
        )

        assert response.status_code == 404

    def test_delete_activity_success(self, client):
        """Test deleting an activity."""
        project_response = client.post("/projects", json={"name": "Test Project"})
        project_id = project_response.json()["id"]

        activity_response = client.post(
            f"/projects/{project_id}/activities",
            json={
                "name": "Task 1",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 45,
                "actual_cost": 400,
            },
        )
        activity_id = activity_response.json()["id"]

        response = client.delete(f"/activities/{activity_id}")

        assert response.status_code == 204

        get_response = client.get(f"/activities/{activity_id}")
        assert get_response.status_code == 404

    def test_delete_activity_not_found(self, client):
        """Test deleting non-existent activity."""
        response = client.delete("/activities/9999")

        assert response.status_code == 404

    def test_project_consolidation_correct(self, client):
        """Test that project consolidation uses sum-then-calculate, NOT averages.

        Creates project with 2 activities:
        Activity 1: EV=400, AC=500 → CPI=0.80
        Activity 2: EV=2000, AC=1000 → CPI=2.00

        Consolidation MUST be:
        - Total EV = 2400, Total AC = 1500
        - CPI = 2400/1500 = 1.60
        - Average would be (0.80 + 2.00) / 2 = 1.40 ≠ 1.60
        """
        project_response = client.post(
            "/projects", json={"name": "Consolidation Test"}
        )
        project_id = project_response.json()["id"]

        client.post(
            f"/projects/{project_id}/activities",
            json={
                "name": "Activity 1",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 40,
                "actual_cost": 500,
            },
        )

        client.post(
            f"/projects/{project_id}/activities",
            json={
                "name": "Activity 2",
                "bac": 5000,
                "planned_percentage": 50,
                "actual_percentage": 40,
                "actual_cost": 1000,
            },
        )

        response = client.get(f"/projects/{project_id}")

        assert response.status_code == 200
        project_data = response.json()
        indicators = project_data["indicators"]

        assert float(indicators["bac"]) == 6000.0
        assert indicators["ev"] == "2400.00"
        assert float(indicators["ac"]) == 1500.0
        assert indicators["cpi"] == "1.60"

        average_cpi = (Decimal("0.80") + Decimal("2.00")) / Decimal("2")
        assert indicators["cpi"] != str(average_cpi)
