from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.tasks.models import Task

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="testuser@gmail.com",
        password="testpassword123",
        first_name="Tyrion",
        last_name="Lannister",
    )


@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.mark.django_db
class TestTaskAPI:
    def test_create_task_success(self, auth_client, test_user):
        due_date = (timezone.now().date() + timedelta(days=1)).isoformat()
        data = {
            "name": "Write unit tests",
            "description": "Cover API endpoints",
            "priority": "HIGH",
            "status": "TODO",
            "due_date": due_date,
        }

        response = auth_client.post("/api/tasks/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["message"] == "Task created successfully"
        assert response.data["data"]["name"] == data["name"]

        task = Task.objects.get(id=response.data["data"]["id"])
        assert task.user == test_user

    def test_create_task_missing_name(self, auth_client):
        data = {"description": "No name provided"}

        response = auth_client.post("/api/tasks/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "Request failed"
        assert "name" in response.data["errors"]

    def test_list_tasks_returns_only_user_tasks(self, auth_client, test_user):
        # Create tasks for test_user
        Task.objects.create(user=test_user, name="Task A")
        Task.objects.create(user=test_user, name="Task B")

        # Create a task for a different user
        other = User.objects.create_user(email="other@test.com", password="pass123")
        Task.objects.create(user=other, name="Other's task")

        response = auth_client.get("/api/tasks/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Tasks retrieved successfully"
        results = response.data["data"]["results"]
        assert len(results) == 2
        names = {r["name"] for r in results}
        assert "Task A" in names and "Task B" in names

    def test_retrieve_update_delete_task(self, auth_client, test_user):
        task = Task.objects.create(user=test_user, name="Original")

        # Retrieve
        retrieve_response = auth_client.get(f"/api/tasks/{task.id}/")
        assert retrieve_response.status_code == status.HTTP_200_OK
        assert retrieve_response.data["data"]["name"] == "Original"

        # Update
        update_data = {"name": "Updated name"}
        update_response = auth_client.patch(f"/api/tasks/{task.id}/", update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["data"]["name"] == "Updated name"

        # Delete
        delete_response = auth_client.delete(f"/api/tasks/{task.id}/")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task.id).exists()

    def test_unauthenticated_access_is_denied(self, api_client):
        response = api_client.get("/api/tasks/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
