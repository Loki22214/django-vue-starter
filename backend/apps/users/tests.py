import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

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
    """Returns an authenticated client"""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.mark.django_db
class TestRegistration:
    """Test user registration endpoint"""

    def test_register_user_success(self, api_client):
        data = {
            "email": "newuser@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post("/api/auth/register/", data)

        # Verify response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["message"] == "User registered successfully"

        # Verify user was created
        user = User.objects.get(email="newuser@example.com")
        assert user.email == "newuser@example.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.check_password("testpass123") is True

    def test_register_user_duplicate_email(self, api_client, test_user):
        data = {
            "email": test_user.email,
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post("/api/auth/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "Registration failed"
        assert "email" in response.data["errors"]

    def test_register_user_password_mismatch(self, api_client):
        data = {
            "email": "newuser@example.com",
            "password": "testpass123",
            "password_confirm": "differentpass",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post("/api/auth/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "Registration failed"
        assert "password" in response.data["errors"]


@pytest.mark.django_db
class TestLogin:
    """Test user login endpoint"""

    def test_login_success(self, api_client, test_user):
        data = {"email": test_user.email, "password": "testpassword123"}

        response = api_client.post("/api/auth/login/", data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Login successful"
        assert "access" in response.data["data"]
        assert "user" in response.data["data"]
        assert response.data["data"]["user"]["email"] == test_user.email

        # Verify refresh token cookie is set
        assert "refresh_token" in response.cookies
        cookie = response.cookies["refresh_token"]
        assert cookie["httponly"] is True
        assert cookie["path"] == "/api/auth/"
        assert cookie["max-age"] == 7 * 24 * 60 * 60

    def test_login_invalid_email(self, api_client):
        data = {"email": "nonexistent@example.com", "password": "gojohnnygo"}

        response = api_client.post("/api/auth/login/", data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_invalid_password(self, api_client, test_user):
        data = {"email": test_user.email, "password": "wrongpassword"}

        response = api_client.post("/api/auth/login/", data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_credentials(self, api_client):
        response = api_client.post("/api/auth/login/", {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRefreshToken:
    """Test token refresh endpoint"""

    def test_refresh_token_success(self, api_client, test_user):
        # Login to obtain the refresh-token cookie
        login_data = {
            "email": test_user.email,
            "password": "testpassword123",
        }
        login_response = api_client.post("/api/auth/login/", login_data)

        assert login_response.status_code == status.HTTP_200_OK
        assert "refresh_token" in login_response.cookies

        # Refresh access token using the cookie retained by APIClient
        refresh_response = api_client.post("/api/auth/refresh/")

        assert refresh_response.status_code == status.HTTP_200_OK
        assert refresh_response.data["success"] is True
        assert "access" in refresh_response.data["data"]
        assert "refresh_token" in refresh_response.cookies

    def test_refresh_token_invalid(self, api_client):
        # Try to refresh without token
        response = api_client.post("/api/auth/refresh/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False
        assert response.data["message"] == "Refresh token not provided."

    def test_refresh_token_expired(self, api_client):
        # Simulate expired token
        expired_token = "some.expired.token"
        api_client.cookies["refresh_token"] = expired_token

        response = api_client.post("/api/auth/refresh/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False


@pytest.mark.django_db
class TestLogout:
    """Test user logout endpoint"""

    def test_logout_success(self, auth_client, test_user):
        # Get refresh token first (simplified - in real scenario you'd login)
        refresh = RefreshToken.for_user(test_user)
        auth_client.cookies["refresh_token"] = str(refresh)

        response = auth_client.post("/api/auth/logout/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Logout successful"
        assert "refresh_token" in response.cookies
        # Cookie should be deleted (expired)
        assert response.cookies["refresh_token"]["max-age"] == 0

    def test_logout_unauthenticated(self, api_client):
        response = api_client.post("/api/auth/logout/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_invalid_token(self, auth_client):
        auth_client.cookies["refresh_token"] = "invalid.token.here"

        response = auth_client.post("/api/auth/logout/")

        assert response.status_code == status.HTTP_200_OK  # Should still succeed
        assert "refresh_token" in response.cookies
        assert response.cookies["refresh_token"]["max-age"] == 0


@pytest.mark.django_db
class TestMeView:
    """Test authenticated user info endpoint"""

    def test_me_view_success(self, auth_client, test_user):
        response = auth_client.get("/api/auth/me/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "User retrieved successfully"
        assert response.data["data"]["email"] == test_user.email
        assert response.data["data"]["first_name"] == test_user.first_name
        assert response.data["data"]["last_name"] == test_user.last_name

    def test_me_view_unauthenticated(self, api_client):
        response = api_client.get("/api/auth/me/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_view_user_data_structure(self, auth_client, test_user):
        response = auth_client.get("/api/auth/me/")

        # Verify all expected fields are present
        data = response.data["data"]
        assert "id" in data
        assert "email" in data
        assert "first_name" in data
        assert "last_name" in data
        assert "date_joined" in data


@pytest.mark.django_db
class TestUserModel:
    """Test user model directly"""

    def test_create_user_success(self):
        user = User.objects.create_user(email="tyrionlannister@gmail.com", password="theimp123")

        assert user.email == "tyrionlannister@gmail.com"
        assert user.check_password("theimp123") is True
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        user = User.objects.create_superuser(email="admin@example.com", password="adminpass123")

        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True

    def test_create_user_without_email(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="testpass")
